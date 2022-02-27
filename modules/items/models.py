from tortoise.models import Model
from tortoise import fields


# aerich init -t settings.TORTOISE_ORM
# aerich init-db   * it means start using aerich and create all edfault staff for it
# aerich migrate   * it means create migrations
# aerich upgrade   * it means run migrations
# aerich downgrade * it means roll back last migrations
# aerich history
# aerich heads     * show migrations that not applyed yed
class Item(Model):
    title = fields.CharField(max_length=150)
    # number = fields.IntField(default=0)
    date_created = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", related_name="items")
