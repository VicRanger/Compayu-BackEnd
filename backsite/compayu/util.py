from .models import Thought
from channels.db import database_sync_to_async

@database_sync_to_async
def writeThoughtAsync(data):
    obj = Thought(
        type_raw=data['type_raw'],
        text=data['text'],
    )
    obj.save()
    return obj


def writeThought(data):
    obj = Thought(
        type_raw=data['type_raw'],
        text=data['text'],
    )
    obj.save()
    return obj
