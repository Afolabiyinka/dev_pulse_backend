from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import auth_service
from app.auth.auth_validation import LoginRequest, SignUpRequest
from app.config import settings
from app.core.cookies_helper import create_auth_cookie
from app.database.db_session import get_db

AuthRouter = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


def signup(
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


def login(
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


def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    return {"message": "Logged out"}


async def github_login():
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": settings.github_redirect_uri,
        "scope": "read:user user:email repo",
    }

    github_url = "https://github.com/login/oauth/authorize?" + urlencode(params)
    return RedirectResponse(github_url)


async def github_callback(
    code: str,
    db: Session = Depends(get_db),
):
    try:
        github_token = await auth_service.exchange_github_code(code)
        user = await auth_service.authenticate_github_user(
            db=db,
            github_token=github_token,
        )

        redirect = RedirectResponse(url=f"{settings.frontend_url}/dashboard")
        create_auth_cookie(redirect, user.id)
        return redirect
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="GitHub authentication failed") from error


AuthRouter.add_api_route("/signup", signup, methods=["POST"], name="Create a new account")
AuthRouter.add_api_route("/login", login, methods=["POST"], name="Login into your account")
AuthRouter.add_api_route("/logout", logout, methods=["POST"], name="Logout from your account")
AuthRouter.add_api_route("/github", github_login, methods=["GET"], name="Login with GitHub")
AuthRouter.add_api_route("/github/callback", github_callback, methods=["GET"], name="Exchange tokens with GitHub")
