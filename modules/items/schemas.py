from tortoise.contrib.pydantic import pydantic_model_creator
from modules.users.models import User as UserModel
from modules.items.models import Item as ItemModel


ItemIn = pydantic_model_creator(ItemModel, name="ItemIn", include=("title", "date_created"))
Item = pydantic_model_creator(ItemModel, name="Item", include=("id", "user_id", "title", "date_created"))


class ItemOutWithUser(Item):
    user: pydantic_model_creator(UserModel, name="UserOut", exclude=("hash_password",))
