# Apply bcrypt compatibility fix FIRST, before any other imports that might use bcrypt
from src.utils import bcrypt_fix  # noqa: F401

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.database import init_db
from src.api.routes import auth_router, tasks_router

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DEBUG: Log configuration on startup
    logger.info("=" * 50)
    logger.info("APPLICATION STARTUP - DIAGNOSTIC INFO")
    logger.info("=" * 50)
    logger.info(f"CORS_ORIGINS from settings: {settings.CORS_ORIGINS}")
    logger.info(f"DEBUG mode: {settings.DEBUG}")
    logger.info(f"DATABASE_URL configured: {'Yes' if settings.DATABASE_URL else 'No'}")
    logger.info(f"JWT_ALGORITHM: {settings.JWT_ALGORITHM}")
    logger.info("=" * 50)
    
    init_db()
    logger.info("Database initialized successfully")
    yield


app = FastAPI(
    title="Todo API",
    description="Full-stack Todo application API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware - Using settings.CORS_ORIGINS instead of hardcoded list
# Parse CORS_ORIGINS from comma-separated string
cors_origins_list = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

# DEBUG: Log the parsed CORS origins
logger.info(f"Parsed CORS origins: {cors_origins_list}")

# Also add hardcoded origins as fallback (without trailing slashes!)
hardcoded_origins = [
    "https://hackathon-ii-todo-app-2-18am-k9i3mq.vercel.app",  # Vercel frontend URL (NO trailing slash!)
    "http://localhost:3000",                                    # For local development
    "http://localhost:8000",                                    # For local backend testing
]

# Combine both lists, removing duplicates
all_origins = list(set(cors_origins_list + hardcoded_origins))
logger.info(f"Final CORS origins list: {all_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/debug/cors")
async def debug_cors(request: Request):
    """Debug endpoint to check CORS configuration and request origin"""
    origin = request.headers.get("origin", "No origin header")
    return {
        "status": "ok",
        "request_origin": origin,
        "configured_origins": all_origins,
        "origin_allowed": origin in all_origins if origin != "No origin header" else "N/A"
    }
