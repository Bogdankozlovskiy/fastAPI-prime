from tortoise.models import Model
from tortoise import fields

# aerich init -t settings.TORTOISE_ORM
# aerich init-db   * it means start using aerich and create all edfault staff for it
# aerich migrate   * it means create migrations
# aerich upgrade   * it means run migrations
# aerich downgrade * it means roll back last migrations
# aerich history
# aerich heads     * show migrations that not applyed yed


class User(Model):
    username = fields.CharField(max_length=150, unique=True)
    hash_password = fields.CharField(max_length=150)
    email = fields.CharField(max_length=150, unique=True)
    full_name = fields.CharField(max_length=150)
    is_active = fields.BooleanField(default=True)
    date_created = fields.DatetimeField(auto_now_add=True)
    date_update = fields.DatetimeField(auto_now=True)
