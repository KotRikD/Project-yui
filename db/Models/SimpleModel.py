from . import BaseModel
import peewee

class MyModel(BaseModel):
    string_model = peewee.CharField(default="lol")
    user_id = peewee.BigIntegerField(unique=True)
