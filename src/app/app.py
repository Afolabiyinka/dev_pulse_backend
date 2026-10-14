from app.core.config import envVariables
from fastapi import FastAPI
from app.modules.auth.auth_routes import AuthRouter
from app.modules.account.account_routes import  AccountRouter
from app.modules.github.github_routes import GithubRouter
from app.core.exception_handlers import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from app.core.rate_limiter import (
    limiter,
    rate_limit_exceeded_handler,
)
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded


# Defining the server
app = FastAPI(title="DevPulse Backend", version="1.0.0",)

# An exception handler for logging errors
register_exception_handlers(app)

API_V1_PREFIX = "/api/v1"

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    rate_limit_exceeded_handler,
)
app.add_middleware(SlowAPIMiddleware)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        envVariables.frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Setting up mordern api docs
@app.get("/api-docs", include_in_schema=False)
async def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        dark_mode=True,
        layout="sidebar"
    )


# Routing
app.include_router(AuthRouter, prefix=API_V1_PREFIX)
app.include_router(AccountRouter, prefix=API_V1_PREFIX)
app.include_router(GithubRouter, prefix=API_V1_PREFIX)
