from loguru import logger
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.modules.auth import auth_service
from app.modules.auth.auth_validation import LoginRequest, SignUpRequest
from app.core.config import envVariables
from app.core.cookies_helper import create_auth_cookie
from app.database.db_session import get_db
from app.core.rate_limiter import AUTH_RATE_LIMIT, LOGIN_RATE_LIMIT, limiter
from app.core.encryption_helpers import encrypt_token
from app.modules.github import github_services

AuthRouter = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

def github_auth_failure_redirect():
    login_url = f"{envVariables.frontend_url.rstrip('/')}/auth/login"
    return RedirectResponse(
        url=f"{login_url}?{urlencode({'error': 'github_auth_failed'})}"
    )


@AuthRouter.post("/signup", name="Create a new account")
@limiter.limit(AUTH_RATE_LIMIT)
def signup(
    request: Request,
    data: SignUpRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        user = auth_service.register_user(db, data)
        create_auth_cookie(response, user.id)
        return {"message": "Account created successfully"}
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) 
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        ) from error


@AuthRouter.post("/login", name="Login into your account")
@limiter.limit(LOGIN_RATE_LIMIT)
def login(
    request: Request,
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        user = auth_service.authenticate_user(db, data=data)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
        
        create_auth_cookie(response, user.id)
        return {"message": "Logged in"}
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong") from error


@AuthRouter.post("/logout", name="Logout from your account")
@limiter.limit(AUTH_RATE_LIMIT)
def logout(request: Request, response: Response):
    response.delete_cookie("access_token", path="/")
    return {"message": "Logged out"}


@AuthRouter.get("/github", name="Login with GitHub")
@limiter.limit(AUTH_RATE_LIMIT)
async def github_login(request: Request):
    params = {
        "client_id": envVariables.github_client_id,
        "redirect_uri": envVariables.github_redirect_uri,
        "scope": "read:user user:email repo",
    }

    github_url = "https://github.com/login/oauth/authorize?" + urlencode(params)
    return RedirectResponse(github_url)


@AuthRouter.get("/github/callback", name="Exchange tokens with GitHub")
@limiter.limit(AUTH_RATE_LIMIT)
async def github_callback(
    request: Request,
    code: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
):
    if error or not code:
        return github_auth_failure_redirect()

    try:
        github_token = await github_services.exchange_github_code(code)
        encrypted_token = encrypt_token(github_token)

        user = await auth_service.authenticate_github_user(
            db=db,
            github_token=encrypted_token,
        )

        redirect = RedirectResponse(url=f"{envVariables.frontend_url}")
        create_auth_cookie(redirect, user.id)
        return redirect
    except Exception:
        logger.exception("GitHub authentication failed")
        return github_auth_failure_redirect()
