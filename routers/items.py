from fastapi import APIRouter, Body, Depends, status, Response

from schemas import ItemIn, Item, FullUser
from models import Item as ItemModel
from dependencies import get_current_active_user

from typing import List


router = APIRouter(
    prefix="/items",
    tags=['items']
)


@router.post(
    "/create",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {
            "description": "Not authenticated",
            "content": {
                "application/json": {"example": {"error": "Not authenticated"}}
            }
        }
    }
)
async def create_item(item: ItemIn = Body(...), user: FullUser = Depends(get_current_active_user)):
    return await ItemModel.create(**item.dict(), user_id=user.id)


@router.get(
    "/",
    response_model=List[Item],
    operation_id="test_id",
    openapi_extra={"x-aperture-labs-portal": "blue"},
    responses={
        401:  {
            "description": "Not authenticated",
            "content": {
                "application/json": {"example": {"error": "Not authenticated"}}
            }
        }
    }
)
async def get_items(response: Response, user: FullUser = Depends(get_current_active_user)):
    """
    get all items that belongs to current user:

    - **title**: each item must have a title
    - **date created**: date when this item was created
    - **user id**: id of user who owner of this item
    - **id**: id of this item
    \f
    :param user: current User.
    :param response: response for client, we using it for set cookies and headers
    """
    response.set_cookie(key="sessionId", value="sessionValue")
    response.headers['test_header_key'] = "test header value"
    # response.status_code we also can set custom status code if we want
    return await ItemModel.filter(user_id=user.id)
