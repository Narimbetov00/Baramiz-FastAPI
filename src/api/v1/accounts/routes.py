from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from .schemas import UserCreateModel, UserLoginModel
from fastapi.exceptions import HTTPException
from src.db.models import User
from .utils import create_access_token, verify_password,generate_passwd_hash
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user


auth_router = APIRouter()
REFRESH_TOKEN_EXPIRY = 2

@auth_router.post("/signup", status_code=201)
async def create_user_account(user_data: UserCreateModel):
   
    username = user_data.username
    password = user_data.password
    passwd_hash = generate_passwd_hash(password)
    user_exists = await User.get_or_none(username=username)
    if user_exists:
        raise HTTPException(status_code=400,detail="User Already exists")
    
    new_user = await User.create(username=username,password_hash=passwd_hash)
    return {"id":new_user.id,"username":new_user.username,"created_at":new_user.created_at}

    
@auth_router.post("/login")
async def login_users(login_data: UserLoginModel):

    username = login_data.username
    password = login_data.password

    user = await User.get_or_none(username=username)

    if user:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "username": user.username,
                    "user_id": str(user.id),
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "username": user.username,
                    "user_id": str(user.id),
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                    "user": {
                        "username": str(user.username),
                        "id": str(user.id)
                    }
                }
            )

    raise HTTPException(status_code=400,detail="Username Or Password Wrong!")

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer)):
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )

    raise HTTPException(status_code=403,detail="Invalid or Expired token")

@auth_router.get('/me')
async def get_current_user(user=Depends(get_current_user)):
  
    return user
