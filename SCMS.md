# Smart College Management System (SCMS)

## Repository audit

This repository's original application is a Vite/React AI news intelligence platform with a FastAPI backend and SQLAlchemy persistence. It is not a Next.js college platform. The existing backend defaults to SQLite, the frontend is not Next.js, and there is no configured Supabase project, college authentication, or SCMS API. Existing files and behavior are retained; `/scms` is an isolated preview surface.

## Current preview

Run the existing app using `.\run.ps1`, then open `http://127.0.0.1:8000/scms`. During frontend development use `cd frontend; npm run dev` and visit `http://localhost:5173/scms`.

The overview and student directory use clearly labeled fictional sample records in browser memory. Adding a student only changes the current browser session. Attendance, examinations, fees and timetable are honest empty previews: no real records are being stored or processed. This preview is not suitable for real student data.

## Database foundation

`supabase/migrations/202610170001_scms_core.sql` defines a separate PostgreSQL schema for profiles/roles, academic structure, students, faculty assignments, attendance and correction audit, examinations/marks, fee obligations/payments/allocations, timetable, and audit events. Timetable overlaps for room, faculty, and section are rejected by PostgreSQL exclusion constraints. Registration IDs and payment references are unique. Student marks and payment ledger rows are distinct from their parent definitions.

The migration is an unexecuted foundation, not a verified live database. It must be reviewed and applied to a fresh Supabase development project. No Supabase URL, key, or database connection is configured here. RLS policies in the migration require security review before production; in particular, sensitive writes should be mediated by the Python API and database procedures that atomically enforce related ledger, publication, audit, and assignment rules. The current preview does not authenticate users or call this schema.

## Completion status

| Requirement | Current implementation | Verification | Status |
|---|---|---|---|
| Authentication and role boundaries | No SCMS authentication or server authorization | Not implemented or tested | BLOCKED |
| Student management | Search and session-local sample directory; no persistence/API | Frontend build only | PARTIAL |
| Attendance | Schema draft only; no workflow/calculation | Not run | BLOCKED |
| Examinations | Schema draft only; no mark validation/publication | Not run | BLOCKED |
| Fees | Schema draft only; no transactional receipt/ledger workflow | Not run | BLOCKED |
| Timetable | Schema draft has PostgreSQL overlap constraints; no API/UI workflow | Migration not applied | BLOCKED |
| UI/UX | Responsive `/scms` preview, explicit sample-data and no-live-data states | Frontend production build | PARTIAL |
| NVIDIA integration | Existing news platform integration remains separate; no SCMS AI feature | No SCMS live verification | BLOCKED |
| Security | SCMS preview has no real data/authentication; migration policies are unexecuted | No authorization tests | BLOCKED |
| Deployment readiness | No SCMS backend, configured Supabase, or deployment target | Not verified | BLOCKED |

This repository does not satisfy the brief's definition of done. The remaining critical work is the authenticated Python API, business workflows and tests, validated migration/RLS, and replacement of the browser-only preview with persistent API-backed operations. Do not use it as a live college system.

## Intended target architecture

Next.js App Router + TypeScript frontend → FastAPI Python API for validation, authorization, transactions and audit → Supabase PostgreSQL. The current SCMS preview is React/Vite and bypasses the API only for ephemeral sample presentation; no persistence path is implied. NVIDIA should remain an optional server-side integration and must not receive sensitive student records.

## Setup requirements for the next implementation phase

1. Establish the project boundary: migrate the existing repository to the requested Next.js + FastAPI stack while preserving the AI news app under a separate route/repo, or maintain SCMS as an independent app. The current implementation preserves it in place.
2. Create a Supabase development project and configure server-only connection and Auth settings through a local secret store. Never commit credentials.
3. Review and apply the SCMS migration only to the new development database; run SQL policy and concurrency tests.
4. Implement FastAPI endpoints and authenticated workflows before enabling real records.
5. Configure role provisioning through a trusted administrative channel; users must never choose their own role.

## Validation performed

Run `cd frontend; npm run build` for TypeScript checking and the Vite production bundle. The SQL migration has not been executed because a PostgreSQL/Supabase development connection is not configured. No API integration, authentication, authorization, or end-to-end workflow has been verified.
