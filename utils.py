from passlib.context import CryptContext
from typing import Union


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hello_world(msg: Union[str, None] = None) -> None:
    print(f"hello {msg}")
