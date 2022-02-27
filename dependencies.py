from fastapi import Depends, HTTPException, status, BackgroundTasks, Query
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, HTTPBasic, HTTPBasicCredentials

from jose import JWTError, jwt
from datetime import datetime, timezone
from pydantic import ValidationError
from typing import Optional

from modules.users.models import User as UserModel
from modules.users.schemas import UserWithScope, FullUser, JWTToken
from settings import tokenUrl, ALGORITHM, SECRET_KEY, scopes
from utils import hello_world, pwd_context


oauth2_passord_bearer = OAuth2PasswordBearer(tokenUrl=tokenUrl, scopes=scopes, auto_error=False)
security = HTTPBasic(auto_error=False)


class CustomDepends:
    def __init__(self, magick_word):
        self.magick_word = magick_word

    def __call__(self, q: str = Query(None, description="test custom depends")):
        return q is not None and self.magick_word in q


async def get_user(
        token: Optional[str] = Depends(oauth2_passord_bearer),
        credentials: Optional[HTTPBasicCredentials] = Depends(security)
) -> UserWithScope:
    headers = {"WWW-Authenticate": "Bearer"}
    if token is None and credentials is None:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers=headers
            )
    if credentials is not None:
        user = await UserModel.get(username=credentials.username)
        headers = {"WWW-Authenticate": "Basic"}
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="user is not defined",
                headers=headers
            )
        if not pwd_context.verify(credentials.password, user.hash_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="uncorrect username or password",
                headers=headers
            )
        data = await FullUser.from_tortoise_orm(user)
        return UserWithScope(**data.dict(), scopes=list(scopes.keys()))
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
    data = await FullUser.from_tortoise_orm(user)
    return UserWithScope(**data.dict(), scopes=jwt_token.scopes)


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
