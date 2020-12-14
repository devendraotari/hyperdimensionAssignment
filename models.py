from tortoise.models import Model
from tortoise import fields

class ActiveUserCount(Model):
    # Defining `id` field is optional, it will be defined automatically
    # if you haven't done it yourself
    id = fields.IntField(pk=True)
    count = fields.IntField(default=0)

    # Defining ``__str__`` is also optional, but gives you pretty
    # represent of model in debugger and interpreter
    def __str__(self):
        return self.count