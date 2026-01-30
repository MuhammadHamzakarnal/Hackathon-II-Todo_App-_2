import os
import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.database import init_db
from src.api.routes import auth_router, tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Validate required environment variables on startup
    required_vars = ["DATABASE_URL", "BETTER_AUTH_SECRET"]
    missing_vars = [var for var in required_vars if not getattr(settings, var, None)]

    if missing_vars:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

    init_db()
    yield


app = FastAPI(
    title="Todo API",
    description="Full-stack Todo application API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Global exception handler to ensure all errors return JSON
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full traceback for debugging
    print(f"Global exception handler caught: {exc}")
    print(traceback.format_exc())

    # Return JSON response instead of HTML
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

# CORS Middleware - use origins from settings
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


# Root endpoint for Hugging Face Spaces health check
@app.get("/")
async def root():
    return {
        "message": "Todo API is running",
        "status": "healthy",
        "api_endpoints": {
            "health": "/api/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "auth": {
                "register": "POST /api/auth/register",
                "login": "POST /api/auth/login",
                "profile": "GET /api/auth/me"
            },
            "tasks": {
                "list": "GET /api/tasks",
                "create": "POST /api/tasks",
                "update": "PUT /api/tasks/{id}",
                "delete": "DELETE /api/tasks/{id}"
            }
        }
    }
