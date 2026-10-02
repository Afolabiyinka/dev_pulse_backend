from app.config import settings
from app.core.token_helper import create_token
from fastapi  import Response
import uuid
def get_token_cookie_options():
    return {
        "key": "access_token",
        "httponly": True,
        "secure": False if settings.env == "development" else True, # True in prod
        "samesite": "lax",
        "max_age": 60 * 60 * 24 * 7, # 7 days
        "path": "/",
    }



def create_auth_cookie(response: Response, user_id: uuid.UUID):
    token = create_token({
        "userid": str(user_id)
    })

    cookie_options = get_token_cookie_options()

    response.set_cookie(
        value=token,
        **cookie_options
    )