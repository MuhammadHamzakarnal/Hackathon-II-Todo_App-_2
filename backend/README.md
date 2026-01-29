# Backend Setup and Running Instructions

This document explains how to set up and run the backend server for the Todo API application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL database (or another SQL database compatible with SQLModel)

## Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-auth-key-here-make-it-long-and-random
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
DEBUG=false
```

## Running the Server

### Development Mode

To run the server in development mode with auto-reload:

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or from the backend root directory:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

To run the server in production mode:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

Once the server is running, you can access the following endpoints:

- `GET /api/health` - Health check endpoint
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks` - Get all tasks (requires authentication)
- `POST /api/tasks` - Create a new task (requires authentication)
- And more task-related endpoints...

## Testing

To run the tests:

```bash
cd src
python -m pytest ../tests/ -v
```

## Project Structure

```
backend/
├── src/
│   ├── api/          # API route definitions
│   ├── database/     # Database connection and initialization
│   ├── models/       # Data models
│   ├── services/     # Business logic
│   ├── config.py     # Configuration settings
│   └── main.py       # Main application entry point
├── tests/            # Test files
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## Troubleshooting

1. **Database Connection Issues**: Ensure your PostgreSQL server is running and the DATABASE_URL in your .env file is correct.

2. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`.

3. **Port Already in Use**: Change the port number in the uvicorn command if port 8000 is already in use.

4. **CORS Issues**: Update the CORS_ORIGINS in your .env file to include your frontend domain.

5. **SQLModel Relationship Error**: If you encounter an error like `TypeError: Relationship() got an unexpected keyword argument 'cascade_delete'`, this has been fixed in the code by removing the `cascade_delete=True` parameter from the Relationship definition in `src/models/user.py`. This was due to a version compatibility issue with SQLModel.