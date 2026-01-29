
# Backend Specification

## 1. Project Structure

```
backend/
├── __init__.py
├── main.py
├── api/
│   ├── __init__.py
│   ├── endpoints/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── users.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── tasks.py
│       └── users.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── security.py
│   └── security_config.py
├── database/
│   ├── __init__.py
│   ├── session.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   └── test_users.py
│   └── conftest.py
└── requirements.txt
```

## 2. API Endpoints

All endpoints will be under the `/api/v1` path.

### 2.1. Authentication (`/auth`)

- **POST /auth/signup**
  - Description: Register a new user.
  - Request Body: `{
    "username": "string",
    "email": "string",
    "password": "string"
  }`
  - Response Body (Success - 201 Created): `{
    "message": "User created successfully"
  }`
  - Response Body (Error - 400 Bad Request): `{
    "detail": "Username or email already exists"
  }`
  - Response Body (Error - 422 Unprocessable Entity): `{
    "detail": "Validation error"
  }`

- **POST /auth/login**
  - Description: Log in a user and return a JWT token.
  - Request Body: `{
    "email": "string",
    "password": "string"
  }`
  - Response Body (Success - 200 OK): `{
    "access_token": "string",
    "token_type": "bearer"
  }`
  - Response Body (Error - 401 Unauthorized): `{
    "detail": "Incorrect email or password"
  }`

### 2.2. Users (`/users`)

- **GET /users/me**
  - Description: Get the current logged-in user's profile.
  - Authentication: Required (Bearer Token)
  - Response Body (Success - 200 OK): `{
    "id": "integer",
    "username": "string",
    "email": "string"
  }`
  - Response Body (Error - 401 Unauthorized): `{
    "detail": "Not authenticated"
  }`

### 2.3. Tasks (`/tasks`)

- **POST /tasks**
  - Description: Create a new task for the current user.
  - Authentication: Required (Bearer Token)
  - Request Body: `{
    "title": "string",
    "description": "string" (optional),
    "due_date": "string" (ISO format, optional)
  }`
  - Response Body (Success - 201 Created): `{
    "id": "integer",
    "title": "string",
    "description": "string" (optional),
    "due_date": "string" (ISO format, optional),
    "created_at": "string" (ISO format),
    "updated_at": "string" (ISO format),
    "owner_id": "integer"
  }`
  - Response Body (Error - 401 Unauthorized): `{
    "detail": "Not authenticated"
  }`
  - Response Body (Error - 422 Unprocessable Entity): `{
    "detail": "Validation error"
  }`

- **GET /tasks**
  - Description: Get all tasks for the current user.
  - Authentication: Required (Bearer Token)
  - Response Body (Success - 200 OK): `[
    {
      "id": "integer",
      "title": "string",
      "description": "string" (optional),
      "due_date": "string" (ISO format, optional),
      "created_at": "string" (ISO format),
      "updated_at": "string" (ISO format),
      "owner_id": "integer"
    }
  ]`
  - Response Body (Error - 401 Unauthorized): `{
    "detail": "Not authenticated"
  }`

- **GET /tasks/{task_id}**
  - Description: Get a specific task by its ID.
  - Authentication: Required (Bearer Token)
  - Path Parameter: `task_id` (integer)
  - Response Body (Success - 200 OK): `{
    "id": "integer",
    "title": "string",
    "description": "string" (optional),
    "due_date": "string" (ISO format, optional),
    "created_at": "string" (ISO format),
    "updated_at": "string" (ISO format),
    "owner_id": "integer"
  }`
  - Response Body (Error - 401 Unauthorized): `{
    "detail": "Not authenticated"
  }`
  - Response Body (Error - 404 Not Found): `{
    "detail": "Task not found"
  }`

- **PUT /tasks/{task_id}**
  - Description: Update an existing task.
  - Authentication: Required (Bearer Token)
  - Path Parameter: `task_id` (integer)
  - Request Body: `{
    "title": "string" (optional),
    "description": "string" (optional),
    "due_date": "string" (ISO format, optional),
    "completed": "boolean" (optional)
  }`
  - Response Body (Success - 200 OK): `{
    "id": "integer",
    "title": "string",
    "description": "string" (optional),
    "due_date": "string" (ISO format, optional),
    "created_at": "string" (ISO format),
    "updated_at": "string" (ISO format),
    "owner_id": "integer",
    "completed": "boolean"
  }`
  - Response Body (Error - 401 Unauthorized): `{
    "detail": "Not authenticated"
  }`
  - Response Body (Error - 404 Not Found): `{
    "detail": "Task not found"
  }`
  - Response Body (Error - 422 Unprocessable Entity): `{
    "detail": "Validation error"
  }`

- **DELETE /tasks/{task_id}**
  - Description: Delete a task.
  - Authentication: Required (Bearer Token)
  - Path Parameter: `task_id` (integer)
  - Response Body (Success - 204 No Content): ""
  - Response Body (Error - 401 Unauthorized): `{
    "detail": "Not authenticated"
  }`
  - Response Body (Error - 404 Not Found): `{
    "detail": "Task not found"
  }`

## 3. Database Schema (SQLModel)

### `database/models.py`

```python
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship

class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(unique=True, index=True)

class UserCreate(UserBase):
    password: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    tasks: list["Task"] = Relationship(back_populates="owner")

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="tasks")

# Need to ensure datetime objects are properly handled by Pydantic/SQLModel
# For example, using a custom validator or ensuring ISO format strings are used in API requests/responses.
```

## 4. Authentication Mechanisms

- **Password Hashing**: Passwords will be hashed using `bcrypt` for security. The `password` field in the `UserCreate` model will be hashed before being stored in the `hashed_password` field of the `User` model.
- **JWT Tokens**: JSON Web Tokens (JWT) will be used for session management. Upon successful login, a JWT containing the user's ID will be generated and returned to the client. This token will be used for authenticating subsequent requests to protected API endpoints.
- **Security**: The `core/security.py` module will handle password hashing and JWT generation/verification. Sensitive configurations (like JWT secret key and algorithm) will be managed in `core/security_config.py` and loaded via environment variables.

## 5. Deployment Strategy

- **Containerization**: The backend application will be containerized using Docker.
- **Web Server**: Gunicorn will be used as the production WSGI HTTP Server for FastAPI.
- **Database**: Neon PostgreSQL will be used as the managed PostgreSQL database. Connection details (host, port, user, password, database name) will be provided via environment variables.
- **CI/CD**: A CI/CD pipeline (e.g., GitHub Actions) will be set up to automate testing, building Docker images, and deploying to a container orchestration platform (e.g., Docker Compose for development/staging, Kubernetes for production).
- **Environment Variables**: All sensitive information and configuration parameters (database credentials, JWT secret key, etc.) will be managed through environment variables.

## 6. Error Handling

- Consistent error responses will be returned in JSON format, including a `detail` field with a descriptive message.
- Standard HTTP status codes will be used (e.g., 200, 201, 400, 401, 404, 422, 500).
- FastAPI's `HTTPException` will be used for raising errors.

## 7. Testing

- Unit and integration tests will be implemented using `pytest`.
- Tests will cover API endpoints, database interactions, and authentication logic.
- Test coverage will be tracked to ensure comprehensive testing.
- `conftest.py` will be used for setup and teardown logic, including database session management for tests.
