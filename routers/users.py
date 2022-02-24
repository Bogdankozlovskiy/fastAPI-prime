from fastapi import APIRouter, Depends, status, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm


from settings import tokenUrl, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import User, AccessToken, JWTToken, FullUser, UserOut, UserRegister
from models import User as UserModel
from utils import pwd_context
from dependencies import get_current_active_user

from datetime import datetime, timedelta
from jose import jwt

router = APIRouter()


@router.post(tokenUrl, include_in_schema=False, response_model=AccessToken)
async def login(user: OAuth2PasswordRequestForm = Depends()):
    db_user = await UserModel.get(username=user.username)
    db_user_model = User.from_orm(db_user)
    hashed_password = pwd_context.hash(user.password)
    if pwd_context.verify(db_user_model.hash_password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="uncorrect username or password"
        )
    jwt_token = JWTToken(
        sub=db_user_model.username,
        exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    token = jwt.encode(jwt_token.dict(), key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}


@router.get("/users/me", tags=['users'], response_model=UserOut)
async def user_me(user: FullUser = Depends(get_current_active_user)):
    return user


@router.post("/users/register", tags=['users'], response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister = Body(...)):
    return await UserModel.create(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hash_password=pwd_context.hash(user.password._secret_value)
    )
