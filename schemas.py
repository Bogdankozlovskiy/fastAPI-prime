from pydantic import BaseModel, Field, EmailStr, SecretStr
from datetime import datetime


class JWTToken(BaseModel):
    sub: str = Field(...)
    exp: datetime = Field(...)


class AccessToken(BaseModel):
    token_type: str = Field("bearer")
    access_token: str = Field(...)


class ItemIn(BaseModel):
    title: str = Field(...)
    date_created: datetime = Field(...)


class Item(ItemIn):
    id: int = Field(...)
    user_id: int = Field(...)

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: str = Field(...)
    is_active: bool = Field(True)

    class Config:
        orm_mode = True


class User(BaseUser):
    hash_password: str = Field(...)


class UserOut(BaseUser):
    id: int = Field(...)


class FullUser(User, UserOut):
    pass


class UserRegister(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: str = Field(...)
    password: SecretStr = Field(...)
