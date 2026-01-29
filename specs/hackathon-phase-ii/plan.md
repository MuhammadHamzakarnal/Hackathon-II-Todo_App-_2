# Implementation Plan: Hackathon Phase II - Full-Stack Todo App

**Branch**: `main` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/hackathon-phase-ii/spec.md`

## Summary

Build a multi-user task management application with secure JWT authentication, task CRUD operations scoped to authenticated users, and a responsive modern UI. The system uses Next.js (App Router) for frontend, FastAPI for backend, SQLModel ORM with Neon Serverless PostgreSQL for persistence, and bcrypt/JWT for authentication.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, passlib[bcrypt], python-jose (backend); Next.js 16+, React 19, Tailwind CSS 4 (frontend)
**Storage**: Neon Serverless PostgreSQL via SQLModel ORM
**Testing**: pytest (backend), manual/E2E (frontend)
**Target Platform**: Web application (Linux server backend, browser frontend)
**Project Type**: Web (monorepo with backend/ and frontend/ directories)
**Performance Goals**: <100ms p95 API latency, <1s FCP on 3G, 60fps UI animations
**Constraints**: All task queries filtered by user_id, JWT expiration enforced, mobile-first design
**Scale/Scope**: Multi-user, ~1000 concurrent users baseline

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| **Accuracy** | ✅ PASS | API endpoints match spec exactly; schema follows defined structure |
| **Clarity** | ✅ PASS | Layered architecture (routes → services → models) with clear separation |
| **Reproducibility** | ✅ PASS | Environment variables for secrets; containerizable structure |
| **Rigor** | ✅ PASS | bcrypt password hashing; JWT middleware on all protected routes |
| **Performance** | ✅ PASS | Indexed queries; optimized frontend rendering; lazy loading where appropriate |

**Key Standards Compliance**:
- ✅ API endpoints follow spec: `POST /api/auth/register`, `POST /api/auth/login`, `GET/POST/PUT/DELETE /api/tasks`
- ✅ Database schema enforces user-task ownership via foreign key constraint
- ✅ JWT token handling with proper validation and expiration
- ✅ Frontend UI is responsive, modular, and component-based
- ✅ No plain text passwords; JWT secrets in environment variables

## Project Structure

### Documentation (this feature)

```text
specs/hackathon-phase-ii/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (implementation plan)
└── tasks.md             # Task breakdown (to be generated via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Authentication logic (hash, verify, JWT)
│   │   └── task_service.py  # Task CRUD operations
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py  # JWT middleware, DB session
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py      # /api/auth/* endpoints
│   │       └── tasks.py     # /api/tasks/* endpoints
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py      # Neon PostgreSQL connection
│   ├── config.py            # Environment configuration
│   └── main.py              # FastAPI app entry point
└── tests/
    ├── __init__.py
    ├── test_auth.py         # Authentication tests
    └── test_tasks.py        # Task CRUD tests

frontend/
├── app/
│   ├── layout.tsx           # Root layout with providers
│   ├── page.tsx             # Hero landing page
│   ├── login/page.tsx       # Login page
│   ├── signup/page.tsx      # Signup page
│   └── dashboard/page.tsx   # Task dashboard (protected)
├── components/
│   ├── shared/
│   │   ├── Button.tsx       # Reusable button component
│   │   ├── Input.tsx        # Reusable input component
│   │   ├── Modal.tsx        # Reusable modal component
│   │   ├── Toast.tsx        # Toast notifications
│   │   └── index.ts         # Barrel export
│   ├── tasks/
│   │   ├── TaskCard.tsx     # Individual task display
│   │   ├── TaskList.tsx     # Task list container
│   │   ├── TaskForm.tsx     # Add/Edit task form
│   │   └── index.ts         # Barrel export
│   ├── layout/
│   │   ├── Header.tsx       # Navigation header
│   │   └── index.ts         # Barrel export
│   └── auth/
│       ├── AuthForm.tsx     # Login/Signup form component
│       └── index.ts         # Barrel export
├── lib/
│   ├── api.ts               # API client for backend calls
│   └── auth-context.tsx     # Auth context provider (JWT storage)
├── types/
│   └── index.ts             # TypeScript type definitions
└── node_modules/            # Dependencies (not committed)
```

**Structure Decision**: Web application monorepo with separate `backend/` (FastAPI) and `frontend/` (Next.js) directories. This follows Option 2 from the template, appropriate for full-stack web applications.

## Architecture Overview

### Data Flow

```
┌─────────────┐     HTTPS/JWT      ┌─────────────┐     SQLModel      ┌─────────────┐
│   Browser   │ ◄──────────────► │   FastAPI   │ ◄───────────────► │    Neon     │
│  (Next.js)  │                    │   Backend   │                    │  PostgreSQL │
└─────────────┘                    └─────────────┘                    └─────────────┘
      │                                   │
      │ JWT Token                         │ User Context
      │ (localStorage)                    │ (from JWT decode)
      ▼                                   ▼
┌─────────────┐                    ┌─────────────┐
│ Auth Context│                    │  Services   │
│  Provider   │                    │   Layer     │
└─────────────┘                    └─────────────┘
```

### Authentication Flow

1. **Registration**: User submits email/password → Backend hashes password → Stores in DB → Returns JWT
2. **Login**: User submits credentials → Backend verifies hash → Returns JWT
3. **Protected Request**: Frontend includes JWT in Authorization header → Backend middleware decodes → User attached to request
4. **Task Ownership**: All task queries include `WHERE user_id = :current_user_id`

### Security Model

| Layer | Protection | Implementation |
|-------|------------|----------------|
| Password | bcrypt hashing | `passlib.context.CryptContext` |
| API Auth | JWT Bearer tokens | `python-jose` with HS256 |
| Token Storage | HTTP-only consideration / localStorage | Frontend auth context |
| Task Isolation | User-scoped queries | Service layer enforces `user_id` filter |
| CORS | Origin whitelist | FastAPI CORS middleware |

## Implementation Phases

### Phase Summary (Maps to User Steps)

| User Step | Plan Phase(s) | Status |
|-----------|---------------|--------|
| Step 1: Setup Monorepo | Phase 1 | ✅ Complete |
| Step 2: Frontend Development | Phase 5, 7 | ✅ Complete |
| Step 3: Backend Development | Phase 4 | ✅ Complete |
| Step 4: Database Setup | Phase 2 | ✅ Complete |
| Step 5: Authentication | Phase 3, 6 | ✅ Complete |
| Step 6: Testing & QA | Phase 8 | ✅ Complete |
| Step 7: Documentation | Phase 9 | ✅ Complete |

---

### Phase 1: Project Setup & Infrastructure

**Objective**: Establish monorepo structure with working development environment.

| Step | Description | Files Affected |
|------|-------------|----------------|
| 1.1 | Initialize Next.js frontend with App Router | `frontend/` directory |
| 1.2 | Initialize FastAPI backend with SQLModel | `backend/` directory |
| 1.3 | Configure Neon PostgreSQL connection | `backend/src/database/database.py`, `.env` |
| 1.4 | Setup CORS for frontend-backend communication | `backend/src/main.py` |

**Exit Criteria**: Both servers start; frontend can make CORS requests to backend.

### Phase 2: Database Models & Schema

**Objective**: Create SQLModel entities matching the spec's database schema.

| Step | Description | Files Affected |
|------|-------------|----------------|
| 2.1 | Create User model with proper fields | `backend/src/models/user.py` |
| 2.2 | Create Task model with user FK | `backend/src/models/task.py` |
| 2.3 | Configure indexes (email, user_id) | Model definitions |
| 2.4 | Setup database initialization | `backend/src/database/database.py` |

**Exit Criteria**: Tables created in Neon; models pass basic CRUD test.

**Data Model Reference** (from spec):

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);

-- Tasks Table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### Phase 3: Authentication Implementation

**Objective**: Implement secure signup/login with JWT token issuance.

| Step | Description | Files Affected |
|------|-------------|----------------|
| 3.1 | Create auth service (hash, verify, JWT) | `backend/src/services/auth_service.py` |
| 3.2 | Create auth routes (register, login) | `backend/src/api/routes/auth.py` |
| 3.3 | Create JWT middleware dependency | `backend/src/api/dependencies.py` |
| 3.4 | Write auth endpoint tests | `backend/tests/test_auth.py` |

**Exit Criteria**: Can register user, login, receive valid JWT; invalid credentials rejected.

**API Contract** (from spec):

| Method | Endpoint | Auth | Request | Response |
|--------|----------|------|---------|----------|
| POST | `/api/auth/register` | No | `{email, password}` | `{user, token}` |
| POST | `/api/auth/login` | No | `{email, password}` | `{user, token}` |

### Phase 4: Task CRUD Backend

**Objective**: Implement all task endpoints with user-scoped access.

| Step | Description | Files Affected |
|------|-------------|----------------|
| 4.1 | Create task service with CRUD operations | `backend/src/services/task_service.py` |
| 4.2 | Create task routes with JWT protection | `backend/src/api/routes/tasks.py` |
| 4.3 | Implement filtering by completion status | Task routes |
| 4.4 | Write task endpoint tests | `backend/tests/test_tasks.py` |

**Exit Criteria**: All CRUD operations work; tasks isolated per user; filtering works.

**API Contract** (from spec):

| Method | Endpoint | Auth | Request | Response |
|--------|----------|------|---------|----------|
| GET | `/api/tasks` | JWT | - | `Task[]` |
| POST | `/api/tasks` | JWT | `{title, description?}` | `Task` |
| GET | `/api/tasks/{id}` | JWT | - | `Task` |
| PUT | `/api/tasks/{id}` | JWT | `{title?, description?, completed?}` | `Task` |
| DELETE | `/api/tasks/{id}` | JWT | - | `204 No Content` |
| PATCH | `/api/tasks/{id}/complete` | JWT | - | `Task` |

### Phase 5: Frontend UI Components

**Objective**: Build responsive, reusable UI components.

| Step | Description | Files Affected |
|------|-------------|----------------|
| 5.1 | Create shared components (Button, Input, Modal, Toast) | `frontend/components/shared/` |
| 5.2 | Create Hero landing page | `frontend/app/page.tsx` |
| 5.3 | Create auth forms (login/signup) | `frontend/components/auth/AuthForm.tsx` |
| 5.4 | Create task components (Card, List, Form) | `frontend/components/tasks/` |
| 5.5 | Create layout components (Header) | `frontend/components/layout/` |

**Exit Criteria**: All components render correctly; responsive across breakpoints.

### Phase 6: Frontend Authentication Integration

**Objective**: Connect frontend to auth endpoints with JWT management.

| Step | Description | Files Affected |
|------|-------------|----------------|
| 6.1 | Create API client utility | `frontend/lib/api.ts` |
| 6.2 | Create Auth context provider | `frontend/lib/auth-context.tsx` |
| 6.3 | Implement login page | `frontend/app/login/page.tsx` |
| 6.4 | Implement signup page | `frontend/app/signup/page.tsx` |
| 6.5 | Add route protection (redirect if not authenticated) | Dashboard page |

**Exit Criteria**: Users can signup/login; JWT stored; protected routes redirect.

### Phase 7: Task Dashboard Implementation

**Objective**: Build the main task management interface.

| Step | Description | Files Affected |
|------|-------------|----------------|
| 7.1 | Implement dashboard page with task list | `frontend/app/dashboard/page.tsx` |
| 7.2 | Connect task CRUD to backend | Dashboard + API client |
| 7.3 | Implement task filtering UI | Dashboard |
| 7.4 | Add loading states and toast notifications | Dashboard + Toast component |

**Exit Criteria**: Full task CRUD works in UI; filtering works; feedback displayed.

### Phase 8: Testing & QA

**Objective**: Validate all acceptance criteria from spec.

| Step | Description | Validation |
|------|-------------|------------|
| 8.1 | Test authentication flows | All auth acceptance scenarios pass |
| 8.2 | Test task CRUD operations | All CRUD acceptance scenarios pass |
| 8.3 | Test task ownership isolation | User A cannot see User B's tasks |
| 8.4 | Test responsive design | UI correct on 320px-1920px |
| 8.5 | Test error handling | Invalid tokens return 401; errors show toast |

**Exit Criteria**: All verification checklist items from spec pass.

### Phase 9: Documentation & Spec-Kit Maintenance

**Objective**: Maintain documentation and version tracking per Spec-Kit conventions.

| Step | Description | Files Affected |
|------|-------------|----------------|
| 9.1 | Update spec.md with implementation status | `specs/hackathon-phase-ii/spec.md` |
| 9.2 | Update plan.md with any architectural changes | `specs/hackathon-phase-ii/plan.md` |
| 9.3 | Maintain tasks.md completion tracking | `specs/hackathon-phase-ii/tasks.md` |
| 9.4 | Update CLAUDE.md with agent-driven task guidelines | `CLAUDE.md` |
| 9.5 | Create PHR records for significant iterations | `history/prompts/hackathon-phase-ii/` |

**Exit Criteria**: All Spec-Kit artifacts up-to-date; version history maintained.

## Technical Decisions

### Decision 1: JWT Storage Strategy

**Options Considered**:
1. HTTP-only cookies (more secure against XSS)
2. localStorage (simpler implementation)

**Decision**: localStorage via Auth Context
**Rationale**: Simpler for hackathon scope; CORS configuration cleaner; XSS risk mitigated by sanitized inputs.

### Decision 2: State Management

**Options Considered**:
1. Redux/Zustand (full state management)
2. React Context (lightweight)

**Decision**: React Context for auth state
**Rationale**: Only auth state needs global management; tasks fetched per-page; avoids over-engineering.

### Decision 3: API Client Pattern

**Options Considered**:
1. fetch wrapper utility
2. axios with interceptors
3. React Query / SWR

**Decision**: Custom fetch wrapper (`lib/api.ts`)
**Rationale**: Minimal dependencies; full control over JWT header injection; sufficient for app scope.

## Risk Analysis

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| JWT secret exposed | HIGH | LOW | Use environment variables; never commit secrets |
| Task ownership bypass | CRITICAL | LOW | Service layer always filters by user_id; tests verify |
| Database connection issues | MEDIUM | MEDIUM | Neon connection pooling; graceful error handling |

## Non-Goals (Explicit Exclusions)

- Refresh token implementation (single JWT sufficient for hackathon)
- Email verification (direct signup without confirmation)
- Password reset flow (out of Phase II scope)
- Real-time updates (polling/manual refresh sufficient)
- Admin functionality (single user role)

## Success Metrics (from Spec)

| Metric | Target | Measurement |
|--------|--------|-------------|
| SC-001 | Signup → login → create task < 60s | Manual timing |
| SC-002 | API p95 latency < 100ms | Backend logging |
| SC-003 | FCP < 1.0s on 3G | Lighthouse |
| SC-004 | 100% task queries scoped to user | Code review + tests |
| SC-005 | 0% invalid JWT access | Auth tests |
| SC-006 | UI correct 320px-1920px | Manual responsive test |
| SC-007 | All CRUD has feedback | Manual verification |

---

## Implementation Status

All 9 phases have been completed. The full-stack todo application is implemented with:

- **Frontend**: Next.js 16+ with App Router, Tailwind CSS, responsive Hero section
- **Backend**: FastAPI with SQLModel ORM, JWT middleware, user-scoped queries
- **Database**: Neon Serverless PostgreSQL with User and Task tables
- **Authentication**: bcrypt password hashing, JWT token issuance/verification
- **Testing**: pytest test suites for auth and task endpoints
- **Documentation**: Spec-Kit artifacts maintained, PHR records created

**Next Step**: Run `/sp.analyze` to verify cross-artifact consistency.
