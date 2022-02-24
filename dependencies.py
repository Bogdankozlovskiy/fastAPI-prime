from fastapi import Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from datetime import datetime, timezone
from fastapi import Query

from models import User as UserModel
from schemas import JWTToken, FullUser
from settings import tokenUrl, ALGORITHM, SECRET_KEY, scopes
from utils import hello_world


oauth2_passord_bearer = OAuth2PasswordBearer(tokenUrl=tokenUrl, scopes=scopes)


class CustomDepends:
    def __init__(self, magick_word):
        self.magick_word = magick_word

    def __call__(self, q: str = Query(None, description="test custom depends")):
        return q is not None and self.magick_word in q


async def get_user(token: str = Depends(oauth2_passord_bearer)) -> FullUser:
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
    user = await UserModel.get(username=jwt_token.sub)
    if not user:
        raise exception
    return FullUser.from_orm(user)


async def get_current_active_user(
        task: BackgroundTasks,
        user: FullUser = Depends(get_user),
        is_query_contain_wisky: bool = Depends(CustomDepends(magick_word="wisky"))
):
    task.add_task(hello_world, msg=user.username)
    if is_query_contain_wisky:
        print(f"{is_query_contain_wisky=}")
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user in unnactive now",
        headers={"WWW-Authenticate": "Bearer"}
    )
