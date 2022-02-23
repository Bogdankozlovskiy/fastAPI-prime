from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timezone

from settings import tokenUrl, ALGORITHM, SECRET_KEY
from pydantic_models import JWTToken, User
from models import User as UserModel


oauth2_passord_bearer = OAuth2PasswordBearer(tokenUrl=tokenUrl)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user(token: str = Depends(oauth2_passord_bearer)) -> User:
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
    return User.parse_obj(user)


def get_current_active_user(user: User = Depends(get_user)):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user in unnactive now",
        headers={"WWW-Authenticate": "Bearer"}
    )
