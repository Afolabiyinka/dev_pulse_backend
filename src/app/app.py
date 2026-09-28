from .config import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.test_connection import test_database_connection
from app.auth.auth_routes import AuthRouter
import logging
from app.core.logger import setup_logging


app = FastAPI(title="Anime Rec Backend", version="1.0.0",)

# Handle logging to the terminal
setup_logging()
logger = logging.getLogger(__name__)

# Test database on startup
@asynccontextmanager
async def lifespan():
    test_database_connection()
    yield
print(f"Server is running on {settings.port}")

# Routing
app.include_router(AuthRouter)