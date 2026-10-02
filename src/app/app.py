from .config import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.test_connection import test_database_connection
from app.auth.auth_routes import AuthRouter
from .account.account_routes import AccountRouter
from app.core.exception_handlers import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference



app = FastAPI(title="DevPulse Backend", version="1.0.0",)
register_exception_handlers(app)


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

@app.get("/api-docs", include_in_schema=False)
async def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

# Test database on startup
@asynccontextmanager
async def lifespan():
    test_database_connection()
    yield

# Routing
app.include_router(AuthRouter)
app.include_router(AccountRouter)