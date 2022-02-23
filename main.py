from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException, Body

from jose import jwt
from datetime import datetime, timedelta
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from application import app
from utils import get_current_active_user, pwd_context
from schemas import JWTToken, User, AccessToken, UserRegister, Item, ItemIn
from settings import tokenUrl, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models import User as UserModel, Item as ItemModel


@app.post(tokenUrl, include_in_schema=False, response_model=AccessToken)
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
    return AccessToken(access_token=token)


@app.get("/users/me", tags=['users'], response_model=User, response_model_exclude={"hash_password"})
async def user_me(user: User = Depends(get_current_active_user)):
    return user


@app.post("/users/register", tags=['users'], response_model=User, response_model_exclude={"hash_password"})
async def register(user: UserRegister = Body(...)):
    users = await UserModel.filter(username=user.username)
    if users:
        return {"error": "user with this username already exists"}
    user = await UserModel.create(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hash_password=pwd_context.hash(user.password._secret_value)
    )
    return user


@app.post("/items/create", tags=['items'], response_model=Item)
async def create_item(item: ItemIn = Body(...), user: UserModel = Depends(get_current_active_user)):
    return await ItemModel.create(**item.dict(), user_id=user.id)
