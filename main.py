from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, status, HTTPException, Request

from pydantic import BaseModel, Field, EmailStr
from typing import Callable
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from time import time
from passlib.context import CryptContext


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

tokenUrl = "/users/token/login"
oauth2_passord_bearer = OAuth2PasswordBearer(tokenUrl=tokenUrl)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_prcess_time_header(request: Request, call_next: Callable):
    start_time = time()
    respose = await call_next(request)
    process_time = time() - start_time
    respose.headers["X-Process-Time"] = str(process_time)
    return respose


db = {
    "bogdan": {
        "username": "bogdan",
        "Email": "bogdan.k@datarails.com",
        "Hashed Password": "$2b$12$4l1Pkk1io4R4/oTe2IaoYu.ZLo3rhT1Zk8HUdkyfKlWT/bN34BliC",
        "Full Name": "Bogdan Kozlovsky",
        "Is Active": True
    }
}


class JWTToken(BaseModel):
    sub: str = Field(...)
    exp: datetime = Field(...)


class AccessToken(BaseModel):
    token_type: str = Field("bearer")
    access_token: str = Field(...)


class User(BaseModel):
    username: str = Field(..., alias="username")
    email: EmailStr = Field(..., alias="Email")
    full_name: str = Field(..., alias="Full Name")
    is_active: bool = Field(True, alias="Is Active")
    hashed_password: str = Field(..., alias="Hashed Password")


@app.post(tokenUrl, include_in_schema=False, response_model=AccessToken)
async def login(user: OAuth2PasswordRequestForm = Depends()):
    db_user = db.get(user.username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user does not exists"
        )
    db_user_model = User.parse_obj(db_user)
    hashed_password = pwd_context.hash(user.password)
    if pwd_context.verify(db_user_model.hashed_password, hashed_password):
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


def get_user(token: str = Depends(oauth2_passord_bearer)) -> User:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user un authenticated",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise exception
    jwt_token = JWTToken.parse_obj(payload)
    if jwt_token.exp < datetime.now(tz=timezone.utc):
        raise exception
    user = db.get(jwt_token.sub)
    if user is None:
        raise exception
    return User.parse_obj(user)


def get_current_active_user(user: User = Depends(get_user)):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user in unnactive now",
        headers={"WWW-Authenticate": "Bearer"}
    )


@app.get("/users/me", tags=['users'], response_model=User, response_model_exclude={"hashed_password"})
async def user_me(user: User = Depends(get_current_active_user)):
    return user
