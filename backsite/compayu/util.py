from .models import Thought
from channels.db import database_sync_to_async

@database_sync_to_async
def writeThoughtAsync(data):
    obj = Thought()
    for k in data.keys():
        setattr(obj,k,data[k])
    obj.save()
    return obj


def writeThought(data):
    obj = Thought()
    for k in data.keys():
        setattr(obj,k,data[k])
    obj.save()
    return obj
