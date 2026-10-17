-- SCMS academic records schema. Apply to a fresh Supabase project after reviewing
-- the deployment checklist in SCMS.md. Existing project data is not touched.
begin;

create extension if not exists pgcrypto;
create extension if not exists btree_gist;

create type public.scms_role as enum ('admin', 'faculty', 'student', 'accounts', 'exam_staff');
create type public.enrollment_status as enum ('active', 'on_leave', 'withdrawn', 'graduated');
create type public.attendance_status as enum ('present', 'absent', 'late', 'excused');
create type public.exam_state as enum ('draft', 'approved', 'published');

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text not null check (length(trim(full_name)) between 1 and 160),
  role public.scms_role not null default 'student',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.academic_years (
  id uuid primary key default gen_random_uuid(), name text not null unique,
  starts_on date not null, ends_on date not null,
  check (ends_on > starts_on)
);
create table public.courses (
  id uuid primary key default gen_random_uuid(), code text not null unique,
  name text not null, created_at timestamptz not null default now()
);
create table public.sections (
  id uuid primary key default gen_random_uuid(), course_id uuid not null references public.courses(id),
  academic_year_id uuid not null references public.academic_years(id), name text not null,
  unique(course_id, academic_year_id, name)
);
create table public.subjects (
  id uuid primary key default gen_random_uuid(), course_id uuid not null references public.courses(id),
  code text not null, name text not null, semester smallint not null check (semester > 0),
  unique(course_id, code)
);
create table public.students (
  id uuid primary key default gen_random_uuid(), profile_id uuid unique references public.profiles(id),
  registration_number text not null unique check (length(trim(registration_number)) > 0),
  full_name text not null check (length(trim(full_name)) > 0), email text,
  course_id uuid not null references public.courses(id), section_id uuid not null references public.sections(id),
  academic_year_id uuid not null references public.academic_years(id),
  status public.enrollment_status not null default 'active',
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create index students_name_idx on public.students using gin (to_tsvector('simple', full_name));
create index students_section_idx on public.students(section_id, status);

create table public.faculty_assignments (
  id uuid primary key default gen_random_uuid(), faculty_profile_id uuid not null references public.profiles(id),
  subject_id uuid not null references public.subjects(id), section_id uuid not null references public.sections(id),
  academic_year_id uuid not null references public.academic_years(id),
  unique(faculty_profile_id, subject_id, section_id, academic_year_id)
);
create table public.rooms (
  id uuid primary key default gen_random_uuid(), name text not null unique,
  capacity integer not null check (capacity > 0)
);
create table public.timetable_entries (
  id uuid primary key default gen_random_uuid(), subject_id uuid not null references public.subjects(id),
  section_id uuid not null references public.sections(id), faculty_profile_id uuid not null references public.profiles(id),
  room_id uuid not null references public.rooms(id), academic_year_id uuid not null references public.academic_years(id),
  day_of_week smallint not null check (day_of_week between 1 and 7),
  starts_minute smallint not null check (starts_minute between 0 and 1439),
  ends_minute smallint not null check (ends_minute between 1 and 1440 and ends_minute > starts_minute),
  time_range int4range generated always as (int4range(starts_minute, ends_minute, '[)')) stored,
  constraint timetable_room_no_overlap exclude using gist (room_id with =, day_of_week with =, academic_year_id with =, time_range with &&),
  constraint timetable_faculty_no_overlap exclude using gist (faculty_profile_id with =, day_of_week with =, academic_year_id with =, time_range with &&),
  constraint timetable_section_no_overlap exclude using gist (section_id with =, day_of_week with =, academic_year_id with =, time_range with &&)
);

create table public.class_sessions (
  id uuid primary key default gen_random_uuid(), timetable_entry_id uuid references public.timetable_entries(id),
  subject_id uuid not null references public.subjects(id), section_id uuid not null references public.sections(id),
  faculty_profile_id uuid not null references public.profiles(id), held_on date not null,
  cancelled boolean not null default false, created_at timestamptz not null default now(),
  unique(subject_id, section_id, faculty_profile_id, held_on, id)
);
create table public.attendance_records (
  id uuid primary key default gen_random_uuid(), session_id uuid not null references public.class_sessions(id),
  student_id uuid not null references public.students(id), status public.attendance_status not null,
  marked_by uuid not null references public.profiles(id), marked_at timestamptz not null default now(),
  unique(session_id, student_id)
);
create table public.attendance_audit (
  id uuid primary key default gen_random_uuid(), attendance_id uuid not null references public.attendance_records(id),
  changed_by uuid not null references public.profiles(id), old_status public.attendance_status,
  new_status public.attendance_status not null, reason text not null check (length(trim(reason)) >= 5),
  changed_at timestamptz not null default now()
);

create table public.examinations (
  id uuid primary key default gen_random_uuid(), name text not null, academic_year_id uuid not null references public.academic_years(id),
  state public.exam_state not null default 'draft', approved_by uuid references public.profiles(id),
  published_at timestamptz, created_at timestamptz not null default now()
);
create table public.exam_subjects (
  id uuid primary key default gen_random_uuid(), examination_id uuid not null references public.examinations(id),
  subject_id uuid not null references public.subjects(id), max_marks numeric(7,2) not null check (max_marks > 0),
  pass_marks numeric(7,2) not null check (pass_marks >= 0 and pass_marks <= max_marks),
  unique(examination_id, subject_id)
);
create table public.marks (
  id uuid primary key default gen_random_uuid(), exam_subject_id uuid not null references public.exam_subjects(id),
  student_id uuid not null references public.students(id), marks_obtained numeric(7,2) not null check (marks_obtained >= 0),
  entered_by uuid not null references public.profiles(id), updated_at timestamptz not null default now(),
  unique(exam_subject_id, student_id)
);
create table public.marks_audit (
  id uuid primary key default gen_random_uuid(), mark_id uuid not null references public.marks(id),
  changed_by uuid not null references public.profiles(id), old_marks numeric(7,2) not null,
  new_marks numeric(7,2) not null, reason text not null check (length(trim(reason)) >= 5),
  changed_at timestamptz not null default now()
);

create table public.fee_obligations (
  id uuid primary key default gen_random_uuid(), student_id uuid not null references public.students(id),
  description text not null, amount numeric(12,2) not null check (amount > 0), due_on date,
  created_by uuid not null references public.profiles(id), created_at timestamptz not null default now()
);
create table public.payments (
  id uuid primary key default gen_random_uuid(), student_id uuid not null references public.students(id),
  amount numeric(12,2) not null check (amount > 0), transaction_reference text not null unique,
  received_by uuid not null references public.profiles(id), received_at timestamptz not null default now(),
  reversed_at timestamptz, reversal_reason text
);
create table public.payment_allocations (
  payment_id uuid not null references public.payments(id), obligation_id uuid not null references public.fee_obligations(id),
  amount numeric(12,2) not null check (amount > 0), primary key(payment_id, obligation_id)
);
create index payment_student_time_idx on public.payments(student_id, received_at desc);

create table public.audit_logs (
  id uuid primary key default gen_random_uuid(), actor_id uuid references public.profiles(id),
  action text not null, entity_type text not null, entity_id uuid,
  metadata jsonb not null default '{}'::jsonb, created_at timestamptz not null default now()
);
create index audit_logs_entity_idx on public.audit_logs(entity_type, entity_id, created_at desc);

-- Profile creation assigns only the least-privileged role. Role escalation requires
-- a trusted service/admin operation; clients cannot update their own role.
create or replace function public.scms_is_staff(allowed public.scms_role[])
returns boolean language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.profiles p where p.id = (select auth.uid()) and p.role = any(allowed));
$$;

alter table public.profiles enable row level security;
alter table public.academic_years enable row level security;
alter table public.courses enable row level security;
alter table public.sections enable row level security;
alter table public.subjects enable row level security;
alter table public.students enable row level security;
alter table public.faculty_assignments enable row level security;
alter table public.rooms enable row level security;
alter table public.timetable_entries enable row level security;
alter table public.class_sessions enable row level security;
alter table public.attendance_records enable row level security;
alter table public.attendance_audit enable row level security;
alter table public.examinations enable row level security;
alter table public.exam_subjects enable row level security;
alter table public.marks enable row level security;
alter table public.marks_audit enable row level security;
alter table public.fee_obligations enable row level security;
alter table public.payments enable row level security;
alter table public.payment_allocations enable row level security;
alter table public.audit_logs enable row level security;

create policy profiles_self_read on public.profiles for select to authenticated using (id = (select auth.uid()) or public.scms_is_staff(array['admin','faculty','accounts','exam_staff']::public.scms_role[]));
create policy profiles_self_update on public.profiles for update to authenticated using (id = (select auth.uid())) with check (id = (select auth.uid()));
create policy admin_profiles_manage on public.profiles for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));
-- Clients may edit their display name only; role assignment is reserved for a
-- trusted provisioning path using the service role, never a user JWT.
revoke insert, update on public.profiles from authenticated;
grant update (full_name, updated_at) on public.profiles to authenticated;

create policy academic_read on public.academic_years for select to authenticated using (true);
create policy course_read on public.courses for select to authenticated using (true);
create policy section_read on public.sections for select to authenticated using (true);
create policy subject_read on public.subjects for select to authenticated using (true);
create policy room_read on public.rooms for select to authenticated using (true);
create policy admin_academic_write on public.academic_years for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));
create policy admin_course_write on public.courses for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));
create policy admin_section_write on public.sections for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));
create policy admin_subject_write on public.subjects for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));
create policy admin_room_write on public.rooms for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));

create policy student_self_or_staff_read on public.students for select to authenticated using (profile_id = (select auth.uid()) or public.scms_is_staff(array['admin','faculty','accounts','exam_staff']::public.scms_role[]));
create policy admin_student_write on public.students for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));
create policy faculty_assignment_read on public.faculty_assignments for select to authenticated using (faculty_profile_id = (select auth.uid()) or public.scms_is_staff(array['admin']::public.scms_role[]));
create policy admin_assignment_write on public.faculty_assignments for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));
create policy timetable_read on public.timetable_entries for select to authenticated using (true);
create policy admin_timetable_write on public.timetable_entries for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));

create policy sessions_staff_read on public.class_sessions for select to authenticated using (public.scms_is_staff(array['admin','faculty']::public.scms_role[]));
create policy sessions_authorized_insert on public.class_sessions for insert to authenticated with check (public.scms_is_staff(array['admin']::public.scms_role[]) or (faculty_profile_id = (select auth.uid()) and exists (select 1 from public.faculty_assignments fa where fa.faculty_profile_id = (select auth.uid()) and fa.subject_id = class_sessions.subject_id and fa.section_id = class_sessions.section_id)));
create policy attendance_student_or_staff_read on public.attendance_records for select to authenticated using (exists (select 1 from public.students s where s.id = attendance_records.student_id and s.profile_id = (select auth.uid())) or public.scms_is_staff(array['admin','faculty']::public.scms_role[]));
create policy attendance_authorized_write on public.attendance_records for all to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[]) or exists (select 1 from public.class_sessions cs join public.faculty_assignments fa on fa.faculty_profile_id=cs.faculty_profile_id and fa.subject_id=cs.subject_id and fa.section_id=cs.section_id where cs.id=attendance_records.session_id and cs.faculty_profile_id=(select auth.uid()))) with check (public.scms_is_staff(array['admin']::public.scms_role[]) or exists (select 1 from public.class_sessions cs join public.faculty_assignments fa on fa.faculty_profile_id=cs.faculty_profile_id and fa.subject_id=cs.subject_id and fa.section_id=cs.section_id where cs.id=attendance_records.session_id and cs.faculty_profile_id=(select auth.uid())));
create policy attendance_audit_staff_read on public.attendance_audit for select to authenticated using (public.scms_is_staff(array['admin','faculty']::public.scms_role[]));
create policy attendance_audit_staff_insert on public.attendance_audit for insert to authenticated with check (changed_by=(select auth.uid()) and public.scms_is_staff(array['admin','faculty']::public.scms_role[]));

create policy exam_staff_read on public.examinations for select to authenticated using (state='published' or public.scms_is_staff(array['admin','exam_staff']::public.scms_role[]));
create policy exam_admin_staff_write on public.examinations for all to authenticated using (public.scms_is_staff(array['admin','exam_staff']::public.scms_role[])) with check (public.scms_is_staff(array['admin','exam_staff']::public.scms_role[]));
create policy exam_subject_read on public.exam_subjects for select to authenticated using (exists(select 1 from public.examinations e where e.id=examination_id and (e.state='published' or public.scms_is_staff(array['admin','exam_staff']::public.scms_role[]))));
create policy exam_subject_write on public.exam_subjects for all to authenticated using (public.scms_is_staff(array['admin','exam_staff']::public.scms_role[])) with check (public.scms_is_staff(array['admin','exam_staff']::public.scms_role[]));
create policy marks_student_or_staff_read on public.marks for select to authenticated using (exists(select 1 from public.students s where s.id=student_id and s.profile_id=(select auth.uid())) and exists(select 1 from public.exam_subjects es join public.examinations e on e.id=es.examination_id where es.id=exam_subject_id and e.state='published') or public.scms_is_staff(array['admin','exam_staff']::public.scms_role[]));
create policy marks_exam_staff_write on public.marks for all to authenticated using (public.scms_is_staff(array['admin','exam_staff']::public.scms_role[])) with check (public.scms_is_staff(array['admin','exam_staff']::public.scms_role[]));
create policy marks_audit_staff_read on public.marks_audit for select to authenticated using (public.scms_is_staff(array['admin','exam_staff']::public.scms_role[]));
create policy marks_audit_staff_insert on public.marks_audit for insert to authenticated with check (changed_by=(select auth.uid()) and public.scms_is_staff(array['admin','exam_staff']::public.scms_role[]));

create policy fee_student_or_accounts_read on public.fee_obligations for select to authenticated using (exists(select 1 from public.students s where s.id=student_id and s.profile_id=(select auth.uid())) or public.scms_is_staff(array['admin','accounts']::public.scms_role[]));
create policy fee_accounts_write on public.fee_obligations for all to authenticated using (public.scms_is_staff(array['admin','accounts']::public.scms_role[])) with check (public.scms_is_staff(array['admin','accounts']::public.scms_role[]));
create policy payment_student_or_accounts_read on public.payments for select to authenticated using (exists(select 1 from public.students s where s.id=student_id and s.profile_id=(select auth.uid())) or public.scms_is_staff(array['admin','accounts']::public.scms_role[]));
create policy payment_accounts_insert on public.payments for insert to authenticated with check (received_by=(select auth.uid()) and public.scms_is_staff(array['admin','accounts']::public.scms_role[]));
create policy payment_admin_reversal on public.payments for update to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[])) with check (public.scms_is_staff(array['admin']::public.scms_role[]));
create policy allocation_ownership_read on public.payment_allocations for select to authenticated using (exists(select 1 from public.payments p join public.students s on s.id=p.student_id where p.id=payment_id and (s.profile_id=(select auth.uid()) or public.scms_is_staff(array['admin','accounts']::public.scms_role[]))));
create policy allocation_accounts_write on public.payment_allocations for all to authenticated using (public.scms_is_staff(array['admin','accounts']::public.scms_role[])) with check (public.scms_is_staff(array['admin','accounts']::public.scms_role[]));
create policy audit_admin_read on public.audit_logs for select to authenticated using (public.scms_is_staff(array['admin']::public.scms_role[]));
create policy audit_staff_insert on public.audit_logs for insert to authenticated with check (actor_id=(select auth.uid()) and public.scms_is_staff(array['admin','faculty','accounts','exam_staff']::public.scms_role[]));

commit;
