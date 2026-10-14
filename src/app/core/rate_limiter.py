from fastapi import Request
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address



GLOBAL_RATE_LIMIT = "100/minute"

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[GLOBAL_RATE_LIMIT],
)

AUTH_RATE_LIMIT = "10/minute"
LOGIN_RATE_LIMIT = "5/minute"


async def rate_limit_exceeded_handler(
    request: Request,
    exc: Exception,
) -> Response:
    if not isinstance(exc, RateLimitExceeded):
        raise exc

    return _rate_limit_exceeded_handler(request, exc)