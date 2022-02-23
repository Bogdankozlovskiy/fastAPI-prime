from tortoise.models import Model
from tortoise import fields


class User(Model):
    username = fields.CharField(max_length=150)
    hash_password = fields.CharField(max_length=150)
    email = fields.CharField(max_length=150)
    full_name = fields.CharField(max_length=150)
    is_active = fields.BooleanField(default=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_update = fields.DatetimeField(auto_now=True)


class Item(Model):
    title = fields.CharField(max_length=150)
    date_created = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", related_name="items")
