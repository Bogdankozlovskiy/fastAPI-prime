from fastapi import APIRouter, Depends, status, HTTPException, Body, Security
from fastapi.security import OAuth2PasswordRequestForm

from settings import tokenUrl, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import User, AccessToken, JWTToken, UserOut, UserRegister, UserWithScope
from models import User as UserModel
from utils import pwd_context
from dependencies import get_current_user_check_permissions

from datetime import datetime, timedelta
from jose import jwt

router = APIRouter()


@router.post(tokenUrl, include_in_schema=False, response_model=AccessToken)
async def login(user: OAuth2PasswordRequestForm = Depends()):
    db_user = await UserModel.get(username=user.username)
    db_user_model = User.from_orm(db_user)
    if not pwd_context.verify(user.password, db_user_model.hash_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="uncorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    jwt_token = JWTToken(
        sub=db_user_model.username,
        exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        scopes=user.scopes
    )
    token = jwt.encode(jwt_token.dict(), key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}


@router.get("/users/me", tags=['users'], response_model=UserOut)
async def user_me(user: UserWithScope = Security(get_current_user_check_permissions, scopes=["me"])):
    return user


@router.post("/users/register", tags=['users'], response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister = Body(...)):
    return await UserModel.create(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hash_password=pwd_context.hash(user.password._secret_value)
    )
