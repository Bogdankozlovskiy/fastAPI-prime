from fastapi import APIRouter, Body, Depends, status

from schemas import ItemIn, Item, FullUser
from models import Item as ItemModel
from dependencies import get_current_active_user

from typing import List


router = APIRouter(
    prefix="/items",
    tags=['items']
)


@router.post("/create", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemIn = Body(...), user: FullUser = Depends(get_current_active_user)):
    return await ItemModel.create(**item.dict(), user_id=user.id)


@router.get("/", response_model=List[Item])
async def get_items(user: FullUser = Depends(get_current_active_user)):
    return await ItemModel.filter(user_id=user.id)
