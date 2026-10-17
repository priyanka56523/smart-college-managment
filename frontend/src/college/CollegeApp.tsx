import { useMemo, useState } from 'react';
import { Activity, BookOpen, CalendarDays, Check, ChevronDown, CircleDollarSign, ClipboardCheck, GraduationCap, LayoutDashboard, Menu, Plus, Search, Settings, ShieldAlert, Users, X } from 'lucide-react';

type Student = { id: number; name: string; registration: string; program: string; year: string; status: 'Active' | 'On leave' };
const initialStudents: Student[] = [
  { id: 1, name: 'Aarav Sharma', registration: 'SC-2024-0182', program: 'Computer Science', year: 'Year 2 · Section A', status: 'Active' },
  { id: 2, name: 'Meera Nair', registration: 'SC-2024-0217', program: 'Business Administration', year: 'Year 2 · Section B', status: 'Active' },
  { id: 3, name: 'Kabir Patel', registration: 'SC-2023-0094', program: 'Computer Science', year: 'Year 3 · Section A', status: 'On leave' },
  { id: 4, name: 'Ananya Iyer', registration: 'SC-2025-0311', program: 'Applied Mathematics', year: 'Year 1 · Section A', status: 'Active' },
  { id: 5, name: 'Rohan Das', registration: 'SC-2024-0240', program: 'Applied Mathematics', year: 'Year 2 · Section A', status: 'Active' },
];
const nav = [
  { label: 'Overview', icon: LayoutDashboard }, { label: 'Students', icon: GraduationCap }, { label: 'Attendance', icon: ClipboardCheck },
  { label: 'Examinations', icon: BookOpen }, { label: 'Fees', icon: CircleDollarSign }, { label: 'Timetable', icon: CalendarDays },
];

export function CollegeApp() {
  const [page, setPage] = useState('Overview');
  const [students, setStudents] = useState(initialStudents);
  const [query, setQuery] = useState('');
  const [studentStatus, setStudentStatus] = useState('All students');
  const [showAdd, setShowAdd] = useState(false);
  const [notice, setNotice] = useState('');
  const [mobileNav, setMobileNav] = useState(false);
  const filtered = useMemo(() => students.filter(s => `${s.name} ${s.registration} ${s.program}`.toLowerCase().includes(query.toLowerCase()) && (studentStatus === 'All students' || s.status === studentStatus)), [students, query, studentStatus]);
  const addStudent = (form: FormData) => {
    const name = String(form.get('name') || '').trim();
    const registration = String(form.get('registration') || '').trim();
    if (!name || !registration) return;
    if (students.some(s => s.registration.toLowerCase() === registration.toLowerCase())) { setNotice('That registration number is already in this demo list.'); return; }
    setStudents(current => [{ id: Date.now(), name, registration, program: String(form.get('program')), year: 'Year 1 · Unassigned', status: 'Active' }, ...current]);
    setShowAdd(false); setNotice('Student added to this browser session.'); window.setTimeout(() => setNotice(''), 3000);
  };
  return <div className="scms">
    <aside className={`scms-sidebar ${mobileNav ? 'mobile-open' : ''}`}>
      <div className="scms-brand"><div className="brand-mark"><GraduationCap size={21}/></div><div><b>Northstar</b><small>COLLEGE SYSTEMS</small></div><button className="mobile-close" onClick={() => setMobileNav(false)} aria-label="Close menu"><X size={18}/></button></div>
      <div className="tenant-label">ACADEMIC YEAR</div><button className="year-picker">2025 – 2026 <ChevronDown size={15}/></button>
      <div className="nav-label">WORKSPACE</div><nav>{nav.map(item => <button key={item.label} onClick={() => { setPage(item.label); setMobileNav(false); }} className={`nav-item ${page === item.label ? 'active' : ''}`}><item.icon size={18}/><span>{item.label}</span>{item.label === 'Attendance' && <i className="nav-dot"/>}</button>)}</nav>
      <div className="sidebar-bottom"><div className="sidebar-notice"><ShieldAlert size={17}/><div><b>Demo workspace</b><span>Sample records only</span></div></div><button className="nav-item"><Settings size={18}/><span>Settings</span></button><div className="profile-chip"><div className="avatar">AD</div><div><b>Administrator</b><small>Demo account</small></div><ChevronDown size={15}/></div></div>
    </aside>
    {mobileNav && <button className="nav-backdrop" onClick={() => setMobileNav(false)} aria-label="Close navigation"/>}
    <main className="scms-main"><header className="scms-topbar"><button className="menu-trigger" onClick={() => setMobileNav(true)} aria-label="Open menu"><Menu size={20}/></button><div className="breadcrumb">Workspace <span>/</span> <b>{page}</b></div><div className="topbar-right"><span className="today-label">SATURDAY, 17 OCTOBER 2026</span><div className="avatar avatar-small">AD</div></div></header>
      <div className="scms-content"><div className="page-heading"><div><div className="eyebrow">ACADEMIC OPERATIONS <span>•</span> 2025–26</div><h1>{page === 'Overview' ? 'Good morning, Admin' : page}</h1><p>{page === 'Overview' ? 'Here is your college at a glance.' : page === 'Students' ? 'Maintain enrolment records and student profiles.' : `${page} operations and records for the current academic year.`}</p></div>{page === 'Students' && <button className="primary-button" onClick={() => setShowAdd(true)}><Plus size={17}/> Add student</button>}</div>
      {page === 'Overview' ? <Overview onGo={setPage} students={students.length}/> : page === 'Students' ? <Students students={filtered} query={query} onQuery={setQuery} status={studentStatus} onStatus={setStudentStatus} onAdd={() => setShowAdd(true)}/> : <ModulePage page={page}/>}
      <footer className="scms-footer"><span>Northstar College Management</span><span>Academic year 2025–26 <b>·</b> Asia/Kolkata</span></footer></div>
    </main>
    {showAdd && <div className="modal-backdrop" onClick={() => setShowAdd(false)}><form className="student-modal" onSubmit={e => {e.preventDefault(); addStudent(new FormData(e.currentTarget));}} onClick={e => e.stopPropagation()}><div className="modal-heading"><div><div className="eyebrow">STUDENT RECORD</div><h2>Add a student</h2></div><button type="button" className="icon-button" onClick={() => setShowAdd(false)} aria-label="Close"><X size={19}/></button></div><label>Full name<input name="name" placeholder="e.g. Priya Menon" required autoFocus/></label><label>Registration number<input name="registration" placeholder="e.g. SC-2026-0042" required/></label><label>Program<select name="program"><option>Computer Science</option><option>Business Administration</option><option>Applied Mathematics</option></select></label><p className="demo-explainer">This sample form updates the browser session only. Connect a secured API to persist college records.</p><div className="modal-actions"><button type="button" className="secondary-button" onClick={() => setShowAdd(false)}>Cancel</button><button className="primary-button"><Check size={16}/> Add student</button></div></form></div>}
    {notice && <div role="status" className="toast">{notice}</div>}
  </div>;
}

function Overview({ onGo, students }: { onGo:(page:string)=>void; students:number }) {
  return <>
    <div className="demo-banner"><Activity size={17}/><span><b>Preview with sample records</b> — figures on this page are illustrative and are not connected to a college database.</span></div>
    <section className="metric-grid"><Metric title="Enrolled students" value={String(students)} note="Sample directory" icon={<GraduationCap/>} tone="blue"/><Metric title="Attendance today" value="—" note="No live session data" icon={<ClipboardCheck/>} tone="teal"/><Metric title="Fees outstanding" value="—" note="No ledger connected" icon={<CircleDollarSign/>} tone="amber"/><Metric title="Classes today" value="—" note="No timetable connected" icon={<CalendarDays/>} tone="violet"/></section>
    <section className="overview-grid"><div className="panel attention-panel"><div className="panel-title"><div><span className="eyebrow">ATTENTION</span><h2>Needs review</h2></div><span className="quiet-tag">No live data</span></div><div className="empty-state"><div className="empty-icon"><Check size={20}/></div><b>No operational alerts</b><p>Attendance, examinations and fee alerts will appear here when connected to your college data.</p></div><button className="text-action" onClick={() => onGo('Attendance')}>Open attendance <span>→</span></button></div>
      <div className="panel quick-panel"><div className="panel-title"><div><span className="eyebrow">QUICK ACCESS</span><h2>Common tasks</h2></div></div><button onClick={() => onGo('Students')} className="quick-link"><span className="quick-icon blue"><Users size={17}/></span><span><b>Student directory</b><small>Browse enrolment records</small></span><span className="arrow">↗</span></button><button onClick={() => onGo('Attendance')} className="quick-link"><span className="quick-icon green"><ClipboardCheck size={17}/></span><span><b>Record attendance</b><small>Open class attendance</small></span><span className="arrow">↗</span></button><button onClick={() => onGo('Timetable')} className="quick-link"><span className="quick-icon gold"><CalendarDays size={17}/></span><span><b>View timetable</b><small>Review class schedule</small></span><span className="arrow">↗</span></button></div></section>
    <section className="panel directory-preview"><div className="panel-title"><div><span className="eyebrow">DIRECTORY</span><h2>Recently enrolled</h2></div><button className="text-action" onClick={() => onGo('Students')}>View directory <span>→</span></button></div><StudentTable students={initialStudents.slice(0,3)}/></section>
  </>;
}
function Metric({title,value,note,icon,tone}:{title:string;value:string;note:string;icon:React.ReactNode;tone:string}) { return <div className="metric"><div className="metric-top"><span>{title}</span><span className={`metric-icon ${tone}`}>{icon}</span></div><strong>{value}</strong><small>{note}</small></div>; }
function Students({students,query,onQuery,status,onStatus,onAdd}:{students:Student[];query:string;onQuery:(v:string)=>void;status:string;onStatus:(v:string)=>void;onAdd:()=>void}) { return <section className="panel student-list"><div className="list-toolbar"><div className="search-box"><Search size={17}/><input aria-label="Search students" value={query} onChange={e => onQuery(e.target.value)} placeholder="Search name, registration or program"/></div><div className="toolbar-actions"><select aria-label="Filter by status" value={status} onChange={e=>onStatus(e.target.value)}><option>All students</option><option>Active</option><option>On leave</option></select><button className="secondary-button" onClick={onAdd}><Plus size={16}/> Add student</button></div></div><div className="result-count">{students.length} records <span>·</span> Registration directory</div><StudentTable students={students}/>{students.length===0 && <div className="no-results">No students match those filters.</div>}<div className="list-foot">Showing {students.length} of {students.length} records <span>Page 1</span></div></section>; }
function StudentTable({students}:{students:Student[]}) { return <div className="table-wrap"><table><thead><tr><th>STUDENT</th><th>REGISTRATION</th><th>PROGRAM</th><th>YEAR / SECTION</th><th>STATUS</th></tr></thead><tbody>{students.map(s=><tr key={s.id}><td><div className="student-name"><span className="student-initials">{s.name.split(' ').map(n=>n[0]).slice(0,2).join('')}</span><b>{s.name}</b></div></td><td className="registration">{s.registration}</td><td>{s.program}</td><td>{s.year}</td><td><span className={`status ${s.status==='Active'?'status-active':'status-leave'}`}><i/>{s.status}</span></td></tr>)}</tbody></table></div>; }
function ModulePage({page}:{page:string}) { const descriptions:Record<string,string>={Attendance:'Record class sessions and review student attendance rates.',Examinations:'Manage assessments, marks and result publication.',Fees:'Track fee obligations, payments and outstanding balances.',Timetable:'Plan class schedules and check room, faculty and section availability.'}; return <><div className="demo-banner"><ShieldAlert size={17}/><span><b>Module preview</b> — this area requires a secured Python API, authenticated roles and a configured PostgreSQL database before it can process real records.</span></div><div className="module-layout"><section className="panel module-intro"><div className="module-icon"><BookOpen size={23}/></div><span className="eyebrow">{page.toUpperCase()} MANAGEMENT</span><h2>{page} workspace</h2><p>{descriptions[page]}</p><div className="module-checklist"><div><Check size={15}/> Domain schema included in project plan</div><div><Activity size={15}/> Live data connection not configured</div></div></section><section className="panel module-empty"><div className="empty-icon"><BookOpen size={20}/></div><b>No {page.toLowerCase()} data connected</b><p>When the API and college database are configured, records and actions for this module will appear here.</p></section></div></>; }
