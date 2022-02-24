from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from datetime import datetime, timezone

from models import User as UserModel
from schemas import JWTToken, FullUser
from settings import tokenUrl, ALGORITHM, SECRET_KEY


oauth2_passord_bearer = OAuth2PasswordBearer(tokenUrl=tokenUrl)


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


def get_current_active_user(user: FullUser = Depends(get_user)):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user in unnactive now",
        headers={"WWW-Authenticate": "Bearer"}
    )
