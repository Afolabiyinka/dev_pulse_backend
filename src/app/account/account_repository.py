from sqlalchemy import select
from sqlalchemy.orm import Session
from app.account.user_model import User

def get_user_by_email(email, db:Session):
    existing_user = db.scalar(
           select(User).where(User.email == email)
       )
    return existing_user

def get_user_by_id(id, db: Session):
   existing_user = db.scalar(
           select(User).where(User.id == id)
       )
   return existing_user