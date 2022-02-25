from fastapi import Depends, HTTPException, status, BackgroundTasks, Query
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from jose import JWTError, jwt
from datetime import datetime, timezone
from pydantic import ValidationError

from models import User as UserModel
from schemas import JWTToken, UserWithScope, FullUser
from settings import tokenUrl, ALGORITHM, SECRET_KEY, scopes
from utils import hello_world


oauth2_passord_bearer = OAuth2PasswordBearer(tokenUrl=tokenUrl, scopes=scopes)


class CustomDepends:
    def __init__(self, magick_word):
        self.magick_word = magick_word

    def __call__(self, q: str = Query(None, description="test custom depends")):
        return q is not None and self.magick_word in q


async def get_user(token: str = Depends(oauth2_passord_bearer)) -> UserWithScope:
    headers = {"WWW-Authenticate": "Bearer"}
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        jwt_token = JWTToken.parse_obj(payload)
    except (JWTError, ValidationError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers=headers
        )
    if jwt_token.exp < datetime.now(tz=timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token was expired",
            headers=headers
        )
    user = await UserModel.get(username=jwt_token.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user is not defined",
            headers=headers
        )
    return UserWithScope(**FullUser.from_orm(user).dict(), scopes=jwt_token.scopes)


async def get_current_active_user(
        task: BackgroundTasks,
        user: UserWithScope = Depends(get_user),
        is_query_contain_wisky: bool = Depends(CustomDepends(magick_word="wisky"))
) -> UserWithScope:
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


async def get_current_user_check_permissions(
        security_scopes: SecurityScopes,
        user: UserWithScope = Depends(get_current_active_user)
) -> UserWithScope:
    required_scopes = set(security_scopes.scopes)
    if required_scopes.issubset(user.scopes):
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="you don't have enough permissions for this action",
        headers={"WWW-Authenticate": f"Bearer scopes={security_scopes.scope_str}"}
    )
