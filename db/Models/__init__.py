from . import *
from common.Store import store
import peewee

class BaseModel(peewee.Model):
    class Meta:
        database = store.config.db

async def get_or_none(model, *args, **kwargs):
    try:
        return await store.config.db.get(model, *args, **kwargs)
    except peewee.DoesNotExist:
        return None



from .SimpleModel import *