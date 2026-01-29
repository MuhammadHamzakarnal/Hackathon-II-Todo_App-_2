from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.database import init_db
from src.api.routes import auth_router, tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Todo API",
    description="Full-stack Todo application API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
origins = [
    "https://frontend-gcohfcq16-haroon-khans-projects-5c7a0028.vercel.app",  # Vercel frontend URL
    "http://localhost:3000",                                             # For local development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
