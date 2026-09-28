from fastapi import  Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.auth.auth_validation import SignUpRequest, LoginRequest
from app.core import token_helper
from app.core import cookies_helper

from app.auth import auth_service
from app.database.db_session import get_db
from app.core.cookies_helper import create_auth_cookie

def signup(
    data: SignUpRequest,
     response: Response,
    db: Session = Depends(get_db),
   
):
  try: 
    user = auth_service.register_user(db, data)
    create_auth_cookie(response, user.id)
    return {"message": "Account created succesfully"}
  
  except ValueError as error:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) 

  except Exception as error:
   print(f"Failed to create account: {error}")
   raise HTTPException(status_code=500, detail="Something went wrong")
    

def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
  try:
    user = auth_service.authenticate_user(db, data.email, data.password)
    if not user :
      raise HTTPException(status_code=401, detail="Invalid Credentials")
    create_auth_cookie(response, user.id)
    return {"Message": "Logged in"}
  except HTTPException:
   raise
  except Exception as error:
    print(f"Login failed: {error}")
    raise HTTPException(status_code=500, detail="Something went wrong")

def logout(response: Response):
  response.delete_cookie("access_token", path="/")
  return {"Message": "Logged Out"}



