# Tasks: Hackathon Phase II - Full-Stack Todo App

**Input**: Design documents from `/specs/hackathon-phase-ii/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are included where specified in the plan (backend tests via pytest).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/` (Next.js App Router)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create monorepo structure with backend/ and frontend/ directories per plan.md
- [X] T002 [P] Initialize Next.js 16+ frontend with App Router in frontend/
- [X] T003 [P] Initialize FastAPI backend with SQLModel dependencies in backend/
- [X] T004 [P] Create .env.example with required environment variables (DATABASE_URL, JWT_SECRET, CORS_ORIGINS)
- [X] T005 [P] Configure TypeScript types in frontend/types/index.ts

**Checkpoint**: Both project directories initialized with dependencies ✅

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Configure Neon PostgreSQL connection in backend/src/database/database.py
- [X] T007 [P] Create environment configuration module in backend/src/config.py
- [X] T008 [P] Create User SQLModel with id, email, password_hash, created_at in backend/src/models/user.py
- [X] T009 [P] Create Task SQLModel with id, user_id (FK), title, description, completed, timestamps in backend/src/models/task.py
- [X] T010 Setup model exports in backend/src/models/__init__.py
- [X] T011 Configure FastAPI app entry point with CORS middleware in backend/src/main.py
- [X] T012 [P] Create API client utility with JWT header injection in frontend/lib/api.ts
- [X] T013 [P] Create shared Button component in frontend/components/shared/Button.tsx
- [X] T014 [P] Create shared Input component in frontend/components/shared/Input.tsx
- [X] T015 [P] Create shared Modal component in frontend/components/shared/Modal.tsx
- [X] T016 [P] Create shared Toast component in frontend/components/shared/Toast.tsx
- [X] T017 Create shared components barrel export in frontend/components/shared/index.ts
- [X] T018 [P] Create Header layout component in frontend/components/layout/Header.tsx
- [X] T019 Create layout components barrel export in frontend/components/layout/index.ts
- [X] T020 Configure root layout with providers in frontend/app/layout.tsx

**Checkpoint**: Foundation ready - database connected, models defined, shared components available ✅

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Allow users to create accounts and log in securely with JWT tokens

**Independent Test**: Create account → Login → Verify JWT token issuance → Access protected route → Verify 401 on expired token

### Backend Implementation for US1

- [X] T021 [P] [US1] Create password hashing utilities (hash, verify) using bcrypt in backend/src/services/auth_service.py
- [X] T022 [US1] Implement JWT token creation and verification in backend/src/services/auth_service.py
- [X] T023 [US1] Create user registration function in backend/src/services/auth_service.py
- [X] T024 [US1] Create user login function in backend/src/services/auth_service.py
- [X] T025 [US1] Create JWT middleware dependency (get_current_user) in backend/src/api/dependencies.py
- [X] T026 [US1] Create database session dependency in backend/src/api/dependencies.py
- [X] T027 [US1] Implement POST /api/auth/register endpoint in backend/src/api/routes/auth.py
- [X] T028 [US1] Implement POST /api/auth/login endpoint in backend/src/api/routes/auth.py
- [X] T029 [US1] Register auth router in backend/src/main.py
- [X] T030 [US1] Write authentication tests (register, login, invalid credentials) in backend/tests/test_auth.py

### Frontend Implementation for US1

- [X] T031 [P] [US1] Create AuthForm component for login/signup in frontend/components/auth/AuthForm.tsx
- [X] T032 [US1] Create auth components barrel export in frontend/components/auth/index.ts
- [X] T033 [US1] Create Auth context provider with JWT storage in frontend/lib/auth-context.tsx
- [X] T034 [US1] Implement signup page with form validation in frontend/app/signup/page.tsx
- [X] T035 [US1] Implement login page with form validation in frontend/app/login/page.tsx
- [X] T036 [US1] Add route protection redirect logic for unauthenticated users

**Checkpoint**: Users can register, login, receive JWT, and are redirected when not authenticated ✅

---

## Phase 4: User Story 2 - Task CRUD Operations (Priority: P1)

**Goal**: Authenticated users can create, view, edit, and delete their own tasks

**Independent Test**: Login → Create task → View task list (own tasks only) → Edit task title → Toggle completion → Delete task

### Backend Implementation for US2

- [X] T037 [US2] Implement create_task function (user-scoped) in backend/src/services/task_service.py
- [X] T038 [US2] Implement get_user_tasks function (filtered by user_id) in backend/src/services/task_service.py
- [X] T039 [US2] Implement get_task_by_id function (user ownership check) in backend/src/services/task_service.py
- [X] T040 [US2] Implement update_task function (user ownership check) in backend/src/services/task_service.py
- [X] T041 [US2] Implement delete_task function (user ownership check) in backend/src/services/task_service.py
- [X] T042 [US2] Implement toggle_task_completion function in backend/src/services/task_service.py
- [X] T043 [US2] Create GET /api/tasks endpoint (list user's tasks) in backend/src/api/routes/tasks.py
- [X] T044 [US2] Create POST /api/tasks endpoint (create task) in backend/src/api/routes/tasks.py
- [X] T045 [US2] Create GET /api/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [X] T046 [US2] Create PUT /api/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [X] T047 [US2] Create DELETE /api/tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [X] T048 [US2] Create PATCH /api/tasks/{id}/complete endpoint in backend/src/api/routes/tasks.py
- [X] T049 [US2] Register tasks router in backend/src/main.py
- [X] T050 [US2] Write task CRUD tests (create, read, update, delete, ownership isolation) in backend/tests/test_tasks.py

### Frontend Implementation for US2

- [X] T051 [P] [US2] Create TaskCard component for individual task display in frontend/components/tasks/TaskCard.tsx
- [X] T052 [P] [US2] Create TaskForm component for add/edit task modal in frontend/components/tasks/TaskForm.tsx
- [X] T053 [US2] Create TaskList component for task list container in frontend/components/tasks/TaskList.tsx
- [X] T054 [US2] Create task components barrel export in frontend/components/tasks/index.ts
- [X] T055 [US2] Implement dashboard page with task list and CRUD operations in frontend/app/dashboard/page.tsx
- [X] T056 [US2] Connect dashboard to backend API for task operations
- [X] T057 [US2] Add task completion toggle functionality to TaskCard

**Checkpoint**: Full task CRUD works; tasks are isolated per user; dashboard shows only user's tasks ✅

---

## Phase 5: User Story 3 - Task Filtering (Priority: P2)

**Goal**: Users can filter their tasks by completion status

**Independent Test**: Create tasks with different completion states → Click filter buttons → Verify correct filtering

### Backend Implementation for US3

- [X] T058 [US3] Add completion status filter parameter to GET /api/tasks endpoint in backend/src/api/routes/tasks.py
- [X] T059 [US3] Update get_user_tasks to support ?completed=true/false query param in backend/src/services/task_service.py

### Frontend Implementation for US3

- [X] T060 [US3] Add filter buttons (All, Pending, Completed) to dashboard in frontend/app/dashboard/page.tsx
- [X] T061 [US3] Implement filter state management and API calls with filter param
- [X] T062 [US3] Update TaskList to display filtered results

**Checkpoint**: Task filtering works; users can view all, pending, or completed tasks ✅

---

## Phase 6: User Story 4 - Responsive Hero Landing (Priority: P2)

**Goal**: Visitors see an attractive, responsive landing page with CTA to signup

**Independent Test**: View landing page on mobile/tablet/desktop → Verify responsive layout → Check logged-in redirect

### Frontend Implementation for US4

- [X] T063 [US4] Create Hero section with headline, description, and CTA buttons in frontend/app/page.tsx
- [X] T064 [US4] Implement responsive design with Tailwind CSS (mobile-first) in frontend/app/page.tsx
- [X] T065 [US4] Add redirect logic for authenticated users to dashboard from landing page
- [X] T066 [US4] Add smooth scroll animations and hover effects to Hero section

**Checkpoint**: Landing page renders correctly on all viewport sizes; logged-in users redirected ✅

---

## Phase 7: User Story 5 - UI Feedback (Priority: P3)

**Goal**: Users receive clear feedback on all operations (success, error, loading)

**Independent Test**: Perform CRUD operations → Observe toast messages → Verify loading indicators

### Frontend Implementation for US5

- [X] T067 [US5] Implement toast notification system (success/error messages) using Toast component
- [X] T068 [US5] Add loading states (spinners/skeletons) during API calls in dashboard
- [X] T069 [US5] Add error handling with user-friendly error messages in API client
- [X] T070 [US5] Connect toast notifications to all CRUD operations in dashboard
- [X] T071 [US5] Add loading indicators to auth forms during submission

**Checkpoint**: All operations show loading states, success toasts, and error messages ✅

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T072 [P] Verify all API endpoints return correct HTTP status codes (400, 401, 404, 500)
- [X] T073 [P] Ensure consistent error response format across all endpoints
- [X] T074 [P] Test responsive design across breakpoints (320px, 768px, 1024px, 1920px)
- [X] T075 [P] Verify JWT expiration handling in both frontend and backend
- [X] T076 Run full acceptance test suite per spec.md verification checklist
- [X] T077 [P] Code cleanup: remove unused imports and console.logs
- [X] T078 Security review: verify no secrets in code, all passwords hashed, task isolation enforced

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✅
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories ✅
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion ✅
  - US1 (Auth) should complete before US2 (Tasks) since tasks require authentication ✅
  - US3 (Filtering) depends on US2 (Tasks) ✅
  - US4 (Hero) can run in parallel with US1/US2 ✅
  - US5 (Feedback) should run after basic CRUD is working ✅
- **Polish (Phase 8)**: Depends on all user stories being complete ✅

### User Story Dependencies

```
Phase 1: Setup ✅
    ↓
Phase 2: Foundational ✅
    ↓
    ├── Phase 3: US1 (Auth) ✅ ← US4 (Hero) can run in parallel ✅
    ↓
    Phase 4: US2 (Task CRUD) ✅ ← Requires US1
    ↓
    ├── Phase 5: US3 (Filtering) ✅ ← Requires US2
    │
    └── Phase 7: US5 (Feedback) ✅ ← Requires US2
    ↓
Phase 8: Polish ✅
```

### Within Each User Story

- Backend implementation before frontend integration
- Services before routes
- Core CRUD before filtering/enhancements
- Tests written alongside implementation

### Parallel Opportunities

**Phase 1 (Setup)**:
- T002, T003, T004, T005 can all run in parallel

**Phase 2 (Foundational)**:
- T007, T008, T009 (config, models) can run in parallel
- T012-T019 (frontend shared components) can all run in parallel

**Phase 3 (US1 - Auth)**:
- T021 (password hashing) can start independently
- T031 (AuthForm) can run in parallel with backend work

**Phase 4 (US2 - Tasks)**:
- T051, T052 (TaskCard, TaskForm) can run in parallel

**Phase 8 (Polish)**:
- T072, T073, T074, T075, T077 can all run in parallel

---

## Parallel Example: User Story 2

```bash
# Launch models in parallel:
T051: "Create TaskCard component in frontend/components/tasks/TaskCard.tsx"
T052: "Create TaskForm component in frontend/components/tasks/TaskForm.tsx"

# After backend services complete (T037-T042):
T043-T048: "Create task API endpoints" (sequential within routes file)

# After frontend components complete:
T053: "Create TaskList component"
T055: "Implement dashboard page"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup ✅
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories) ✅
3. Complete Phase 3: US1 (Authentication) ✅
4. Complete Phase 4: US2 (Task CRUD) ✅
5. **STOP and VALIDATE**: Test auth + task CRUD flow end-to-end ✅
6. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready ✅
2. Add US1 (Auth) → Test auth flow → Demo ✅
3. Add US2 (Task CRUD) → Test CRUD → Deploy/Demo (MVP!) ✅
4. Add US3 (Filtering) → Test filtering → Deploy/Demo ✅
5. Add US4 (Hero) → Test landing → Deploy/Demo ✅
6. Add US5 (Feedback) → Test UX → Deploy/Demo ✅

---

## Summary

| Phase | Story | Task Count | Completed |
|-------|-------|------------|-----------|
| 1 | Setup | 5 | 5 ✅ |
| 2 | Foundational | 15 | 15 ✅ |
| 3 | US1 (Auth) | 16 | 16 ✅ |
| 4 | US2 (Tasks) | 21 | 21 ✅ |
| 5 | US3 (Filtering) | 5 | 5 ✅ |
| 6 | US4 (Hero) | 4 | 4 ✅ |
| 7 | US5 (Feedback) | 5 | 5 ✅ |
| 8 | Polish | 7 | 7 ✅ |
| **Total** | | **78** | **78 ✅** |

### Implementation Status: COMPLETE 🎉

All 78 tasks have been implemented successfully.

### Independent Test Criteria

| Story | Test Criteria | Status |
|-------|---------------|--------|
| US1 | Signup → Login → JWT received → Protected route access → 401 on invalid token | ✅ |
| US2 | Create task → View list (own only) → Edit → Toggle complete → Delete | ✅ |
| US3 | Filter by All → Filter by Pending → Filter by Completed | ✅ |
| US4 | View on mobile → View on desktop → Logged-in redirect | ✅ |
| US5 | See loading states → See success toast → See error message | ✅ |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Backend tests included as specified in plan.md (pytest)
