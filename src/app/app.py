from .config import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.test_connection import test_database_connection
from app.auth.auth_routes import AuthRouter

app = FastAPI(title="Anime Rec Backend", version="1.0.0",)

@asynccontextmanager
async def lifespan():
    test_database_connection()
    yield
print(f"Server is running on {settings.port}")

# Routes
app.include_router(AuthRouter)