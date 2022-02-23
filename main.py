from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException, Body

from jose import jwt
from datetime import datetime, timedelta

from application import app
from utils import get_current_active_user, pwd_context
from schemas import JWTToken, User, UserOut, AccessToken, UserRegister, Item, ItemIn
from settings import tokenUrl, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models import User as UserModel, Item as ItemModel

from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from database import db


@app.post(tokenUrl, include_in_schema=False, response_model=AccessToken)
async def login(user: OAuth2PasswordRequestForm = Depends()):
    exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="uncorrect username or password"
        )
    db_user = await db.fetch_one(select(UserModel))
    if db_user is None:
        raise exception
    db_user_model = User.from_orm(db_user)
    hashed_password = pwd_context.hash(user.password)
    if pwd_context.verify(db_user_model.hash_password, hashed_password):
        raise exception
    jwt_token = JWTToken(
        sub=db_user_model.username,
        exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    token = jwt.encode(jwt_token.dict(), key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}


@app.get("/users/me", tags=['users'], response_model=UserOut)
async def user_me(user: UserModel = Depends(get_current_active_user)):
    return user


@app.post("/users/register", tags=['users'], response_model=UserOut)
async def register(user: UserRegister = Body(...)):
    query = select(UserModel).filter((UserModel.username == user.username) | (UserModel.email == user.email))
    users = await db.fetch_all(query)
    if user.email in {i['email'] for i in users}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with email already exists"
        )
    if user.username in {i['username'] for i in users}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with username already exists"
        )
    query = insert(UserModel).values(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hash_password=pwd_context.hash(user.password._secret_value)
    )
    last_record_id = await db.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.post("/items/create", tags=['items'], response_model=Item)
async def create_item(item: ItemIn = Body(...), user: UserModel = Depends(get_current_active_user)):
    query = insert(ItemModel).values(**item.dict(), user_id=user.id)
    last_record_id = await db.execute(query)
    return {**item.dict(), "user_id": user.id, "id": last_record_id}
