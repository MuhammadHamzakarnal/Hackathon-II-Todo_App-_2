# Todo Backend API

A full-stack Todo application API with JWT authentication built with FastAPI.

## Features

- User authentication (register/login)
- Task management (CRUD operations)
- JWT-based authorization
- PostgreSQL database integration
- CORS support for frontend integration

## Dependencies

- Python 3.9+
- PostgreSQL
- FastAPI
- Uvicorn
- SQLModel
- Pydantic Settings
- Python-Jose (for JWT)
- Passlib (for password hashing)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. Update the `.env` file with your database connection details and secret keys
6. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT signing (should be a long random string)
- `JWT_ALGORITHM`: Algorithm for JWT encoding (default: HS256)
- `JWT_EXPIRY_DAYS`: Number of days for JWT expiry (default: 7)
- `DEBUG`: Enable debug mode (default: False)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

## API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (requires authentication)
- `GET /api/tasks` - Get all tasks for the current user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `DELETE /api/tasks/{task_id}` - Delete a specific task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion status

## Deployment

For deployment on Hugging Face Spaces or similar platforms:
1. Make sure all dependencies are in `requirements.txt`
2. Ensure the Dockerfile is properly configured
3. Set up environment variables in the deployment platform

## License

MIT