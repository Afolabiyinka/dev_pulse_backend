from .config import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.test_connection import test_database_connection
from app.auth.auth_routes import AuthRouter
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings



app = FastAPI(title="DevPulse Backend", version="1.0.0",)

# Cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test database on startup
@asynccontextmanager
async def lifespan():
    test_database_connection()
    yield
logger.info(f"Server is running on {settings.port}")

# Routing
app.include_router(AuthRouter)