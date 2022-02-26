from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.fields.relational import ReverseRelation

from pydantic import BaseModel, Field, EmailStr, SecretStr
from pydantic.utils import GetterDict

from datetime import datetime
from typing import List, Any


class TortoiseGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ReverseRelation):
            return res.related_objects
        return res


class JWTToken(BaseModel):
    sub: str = Field(...)
    exp: datetime = Field(...)
    scopes: List[str] = Field(default_factory=list)


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


class ItemOutWithUser(Item):
    user: "UserOut" = Field(...)


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


class UserOutWithItems(UserOut):
    items: List[Item] = Field(...)

    class Config(UserOut.Config):
        getter_dict = TortoiseGetterDict


class FullUser(User, UserOut):
    pass


class UserWithScope(FullUser):
    scopes: List[str] = Field(default_factory=list)


class UserRegister(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    full_name: str = Field(...)
    password: SecretStr = Field(...)


ItemOutWithUser.update_forward_refs()
