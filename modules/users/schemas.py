from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field, EmailStr, SecretStr
from typing import List
from datetime import datetime

from modules.users.models import User as UserModel
from modules.items.models import Item as ItemModel
from utils import TortoiseGetterDict


class JWTToken(BaseModel):
    sub: str
    exp: datetime
    scopes: List[str] = Field(default_factory=list)


class AccessToken(BaseModel):
    token_type: str = Field("bearer")
    access_token: str


BaseUser = pydantic_model_creator(UserModel, name="BaseUser", include=("username", "email", "full_name", "is_active"))
User = pydantic_model_creator(UserModel, name="User", exclude=("id", ))
UserOut = pydantic_model_creator(UserModel, name="UserOut", exclude=("hash_password",))
FullUser = pydantic_model_creator(UserModel, name="FullUser")


class UserOutWithItems(UserOut):
    items: List[pydantic_model_creator(ItemModel, name="Item", include=("id", "user_id", "title", "date_created"))]

    class Config(UserOut.Config):
        getter_dict = TortoiseGetterDict


class UserWithScope(FullUser):
    scopes: List[str] = Field(default_factory=list)


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: SecretStr
