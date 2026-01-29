# Feature Specification: Task CRUD Feature

**Feature Branch**: `task-crud`
**Created**: 2026-01-16
**Status**: Draft
**Input**: User description: "Implement full CRUD operations for tasks in the Todo app."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Task (Priority: P1)

A logged-in user wants to add a new task to their todo list.

**Why this priority**: Foundation of task management - users must be able to create tasks before any other operations.

**Independent Test**: Can be fully tested by authenticating a user and posting task data to the create endpoint, verifying the task appears in the user's list.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they send a POST request with valid task data, **Then** a new task should be created and returned with 201 status
2. **Given** an authenticated user, **When** they send a POST request with missing required fields, **Then** the system should return 400 with validation errors
3. **Given** an unauthenticated user, **When** they attempt to create a task, **Then** the system should return 401 Unauthorized

---

### User Story 2 - View All Tasks (Priority: P1)

A logged-in user wants to view all their existing tasks.

**Why this priority**: Users need to see what tasks they have to manage them effectively.

**Independent Test**: Can be tested by authenticating a user and calling the list endpoint, verifying only their tasks are returned.

**Acceptance Scenarios**:

1. **Given** an authenticated user with existing tasks, **When** they request their task list, **Then** only their tasks should be returned
2. **Given** an authenticated user with no tasks, **When** they request their task list, **Then** an empty list should be returned
3. **Given** two different users with tasks, **When** each requests their task list, **Then** each user sees only their own tasks

---

### User Story 3 - View Single Task (Priority: P1)

A logged-in user wants to view details of a specific task.

**Why this priority**: Detailed view is essential for managing individual tasks.

**Independent Test**: Can be tested by authenticating a user, creating a task, then fetching it by ID.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an existing task, **When** they request that task by ID, **Then** the full task details should be returned
2. **Given** an authenticated user, **When** they request a task they don't own, **Then** the system should return 404 Not Found
3. **Given** an authenticated user, **When** they request a non-existent task ID, **Then** the system should return 404 Not Found

---

### User Story 4 - Update Task (Priority: P1)

A logged-in user wants to modify an existing task.

**Why this priority**: Users need to be able to edit task details as requirements change.

**Independent Test**: Can be tested by authenticating a user, creating a task, then updating its fields.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an existing task, **When** they send a PUT request to update the task, **Then** the task should be updated and returned
2. **Given** an authenticated user, **When** they attempt to update a task they don't own, **Then** the system should return 404 Not Found
3. **Given** an authenticated user, **When** they send a PUT request with invalid data, **Then** the system should return 400 with validation errors

---

### User Story 5 - Delete Task (Priority: P1)

A logged-in user wants to remove a task from their list.

**Why this priority**: Basic CRUD operation - users need to clean up completed or unwanted tasks.

**Independent Test**: Can be tested by authenticating a user, creating a task, then deleting it and verifying it's gone.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an existing task, **When** they delete that task, **Then** the task should be removed and return 204
2. **Given** an authenticated user, **When** they attempt to delete a task they don't own, **Then** the system should return 404 Not Found
3. **Given** an authenticated user, **When** they delete a task and then request it, **Then** the system should return 404 Not Found

---

### User Story 6 - Toggle Task Completion (Priority: P2)

A logged-in user wants to mark a task as completed or pending.

**Why this priority**: Important feature for task management but can be built after basic CRUD.

**Independent Test**: Can be tested by authenticating a user, creating a task, toggling completion status.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a pending task, **When** they toggle completion, **Then** the task should become completed
2. **Given** an authenticated user with a completed task, **When** they toggle completion, **Then** the task should become pending
3. **Given** an authenticated user, **When** they attempt to toggle a task they don't own, **Then** the system should return 404 Not Found

---

### Edge Cases

- What happens when a user provides a very long title or description?
- How does system handle duplicate task titles for the same user?
- What happens when due_date is in the past?
- How does system handle concurrent updates to the same task?
- What validation is performed on task status values?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow authenticated users to create tasks with title, description, due_date, and status
- **FR-002**: System MUST return only tasks belonging to the authenticated user
- **FR-003**: Users MUST be able to retrieve a single task by ID if they own it
- **FR-004**: System MUST allow task owners to update task attributes
- **FR-005**: System MUST allow task owners to delete their tasks
- **FR-006**: System MUST provide an endpoint to toggle task completion status
- **FR-007**: System MUST validate all task input data
- **FR-008**: System MUST enforce task ownership on all operations
- **FR-009**: System MUST implement JWT-based authentication for all task endpoints

### Key Entities

- **Task**: Represents a todo item with unique ID, title, description, due_date, status (pending/completed), created_at, updated_at, and user_id foreign key
- **User**: Represents an authenticated user who owns tasks

## API Endpoints

- `POST /api/{user_id}/tasks` - Create new task (requires JWT)
- `GET /api/{user_id}/tasks` - List user's tasks (requires JWT)
- `GET /api/{user_id}/tasks/{id}` - Get single task (requires JWT)
- `PUT /api/{user_id}/tasks/{id}` - Update task (requires JWT)
- `DELETE /api/{user_id}/tasks/{id}` - Delete task (requires JWT)
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status (requires JWT)

## Authentication

- All endpoints require valid JWT token
- User ID in token must match {user_id} in path
- Token validation via Better Auth middleware