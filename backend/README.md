# Todo API Backend

This is the backend service for the Todo application, built with FastAPI.

## Features

- User authentication (register/login)
- Task management (CRUD operations)
- JWT-based authentication
- SQLModel for database operations
- CORS configured for frontend integration

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (requires auth)

### Tasks
- `GET /api/tasks` - Get all user tasks (requires auth)
- `POST /api/tasks` - Create a new task (requires auth)
- `PUT /api/tasks/{id}` - Update a task (requires auth)
- `DELETE /api/tasks/{id}` - Delete a task (requires auth)
- `PATCH /api/tasks/{id}/complete` - Toggle task completion (requires auth)

### Health Check
- `GET /api/health` - Check API health status

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Environment Variables

The following environment variables need to be set:

- `DATABASE_URL` - Database connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT tokens
- `CORS_ORIGINS` - Comma-separated list of allowed origins

## Deployment

This backend is designed to run on Hugging Face Spaces with the provided Dockerfile.

The application runs on port 7860 and listens on 0.0.0.0.