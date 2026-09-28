from sqlalchemy.orm import Session
from app.auth.auth_controller import SignUpRequest, LoginRequest
from app.account.account_repository import get_user_by_email
from app.auth.auth_repository import create_user
from app.core.security import verify_password, hash_password


def register_user(
    db: Session,
    data: SignUpRequest,
):
    # Checks if user with the email exists 
    existing_user =  get_user_by_email(email=data.email)
    if existing_user:
        raise ValueError("Email already in use")
 
    hashed = hash_password(data.password)
    
    return create_user(db, data.email, hashed)

def authenticate_user(db: Session, data: LoginRequest):
    user = get_user_by_email(db, data.email, data.password)

# Check  if theres a user and check if the passwords match
    if not user or not verify_password(data.password, user.password):
        return None
    return user