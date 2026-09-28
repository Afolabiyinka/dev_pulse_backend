from fastapi import APIRouter
from app.auth.auth_controller import signup, login, logout

AuthRouter = APIRouter(
    prefix="/auth",
    tags=["Authentication"],

)

AuthRouter.add_api_route("/signup", signup, methods=["POST"],name="Create a new account",)
AuthRouter.add_api_route("/login", login, methods=["POST"], name="Login into your account")