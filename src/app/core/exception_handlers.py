from fastapi import FastAPI, Request
from fastapi.exception_handlers import (
    http_exception_handler as fastapi_http_exception_handler,
)
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(
    request: Request,
    error: Exception,
):
    if isinstance(error, StarletteHTTPException):
        if error.status_code >= 500:
            cause = error.__cause__
            if cause:
                logger.opt(
                    exception=(type(cause), cause, cause.__traceback__)
                ).error(
                    "HTTP {} returned for {} {}",
                    error.status_code,
                    request.method,
                    request.url.path,
                )
            else:
                logger.error(
                    "HTTP {} returned for {} {}: {}",
                    error.status_code,
                    request.method,
                    request.url.path,
                    error.detail,
                )

        return await fastapi_http_exception_handler(request, error)

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


async def unhandled_exception_handler(request: Request, error: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
