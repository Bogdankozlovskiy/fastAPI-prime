from passlib.context import CryptContext
from typing import Union, Any
from pydantic.utils import GetterDict
from tortoise.fields.relational import ReverseRelation


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hello_world(msg: Union[str, None] = None) -> None:
    print(f"hello {msg}")


class TortoiseGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ReverseRelation):
            return res.related_objects
        return res
