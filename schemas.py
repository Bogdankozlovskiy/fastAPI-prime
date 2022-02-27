from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import BaseModel, Field, EmailStr, SecretStr
from datetime import datetime
from typing import List
from utils import TortoiseGetterDict
from models import User as UserModel, Item as ItemModel


class JWTToken(BaseModel):
    sub: str = Field(...)
    exp: datetime = Field(...)
    scopes: List[str] = Field(default_factory=list)


class AccessToken(BaseModel):
    token_type: str = Field("bearer")
    access_token: str = Field(...)


ItemIn = pydantic_model_creator(ItemModel, name="ItemIn", include=("title", "date_created"))
Item = pydantic_model_creator(ItemModel, name="Item", include=("id", "user_id", "title", "date_created"))


class ItemOutWithUser(Item):
    user: "UserOut" = Field(...)


BaseUser = pydantic_model_creator(UserModel, name="BaseUser", include=("username", "email", "full_name", "is_active"))
User = pydantic_model_creator(UserModel, name="User", exclude=("id", ))
UserOut = pydantic_model_creator(UserModel, name="UserOut", exclude=("hash_password",))
FullUser = pydantic_model_creator(UserModel, name="FullUser")


class UserOutWithItems(UserOut):
    items: List[Item] = Field(...)

    class Config(UserOut.Config):
        getter_dict = TortoiseGetterDict


class UserWithScope(FullUser):
    scopes: List[str] = Field(default_factory=list)


class UserRegister(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: str = Field(...)
    password: SecretStr = Field(...)


ItemOutWithUser.update_forward_refs()  # we need to call this mecause in ItemOutWithUser we used postponed annotation
