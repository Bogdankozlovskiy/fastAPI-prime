from fastapi import APIRouter, Depends, status, HTTPException, Body, Security
from fastapi.security import OAuth2PasswordRequestForm

from settings import tokenUrl, ALGORITHM, SECRET_KEY
from modules.users.schemas import User, AccessToken, JWTToken, UserOut, UserRegister, UserWithScope, UserOutWithItems
from modules.users.models import User as UserModel
from utils import pwd_context
from dependencies import get_current_user_check_permissions

from jose import jwt

router = APIRouter()


@router.post(tokenUrl, include_in_schema=False, response_model=AccessToken)
async def login(user: OAuth2PasswordRequestForm = Depends()):
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="uncorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    db_user = await UserModel.get_or_none(username=user.username)
    if db_user is None:
        raise exception
    db_user_model = await User.from_tortoise_orm(db_user)
    if not pwd_context.verify(user.password, db_user_model.hash_password):
        raise exception
    jwt_token = JWTToken(
        sub=db_user_model.username,
        scopes=user.scopes
    )
    token = jwt.encode(jwt_token.dict(), key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "scope": user.scopes}


@router.get("/users/me", tags=['users'], response_model=UserOutWithItems)
async def user_me(user: UserWithScope = Security(get_current_user_check_permissions, scopes=["me"])):
    return await UserModel.filter(id=user.id).prefetch_related("items").first()


@router.post("/users/register", tags=['users'], response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister = Body(...)):
    return await UserModel.create(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hash_password=pwd_context.hash(user.password._secret_value)
    )
