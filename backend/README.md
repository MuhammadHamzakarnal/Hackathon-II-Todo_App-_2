---
title: Todo API Backend
emoji: 🚀
colorFrom: purple
colorTo: yellow
sdk: docker
pinned: false
license: mit
---

# Todo API Backend

This is a FastAPI-based backend for a full-stack Todo application with JWT authentication.

## Features

- JWT-based authentication system
- CRUD operations for todo tasks
- Secure password hashing
- PostgreSQL database integration
- CORS support for frontend integration

## API Endpoints

- `/api/auth/register` - Register a new user
- `/api/auth/login` - Login and get JWT token
- `/api/tasks/` - Get all tasks for authenticated user
- `/api/tasks/create` - Create a new task
- `/api/tasks/{task_id}` - Get a specific task
- `/api/tasks/{task_id}/update` - Update a specific task
- `/api/tasks/{task_id}/delete` - Delete a specific task
- `/api/health` - Health check endpoint

## Environment Variables

The application requires the following environment variables:

- `DATABASE_URL` - PostgreSQL database connection string
- `BETTER_AUTH_SECRET` - Secret key for JWT token signing
- `JWT_ALGORITHM` - Algorithm for JWT encoding (default: HS256)
- `JWT_EXPIRY_DAYS` - Number of days for JWT expiry (default: 7)
- `DEBUG` - Debug mode (default: false)
- `CORS_ORIGINS` - Comma-separated list of allowed origins

## Usage

The backend is deployed and accessible at the root URL of this space. You can make requests to the various API endpoints to interact with the todo application.

## Local Development

To run this application locally:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file
4. Run the application: `uvicorn src.main:app --reload`

## License

MIT