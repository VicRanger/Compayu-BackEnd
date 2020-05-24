from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .util import writeThoughtAsync
from .settings import SendMsgType,ReceiveMsgType

class ThoughtComsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'default_group'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_json({
            'msg_type': SendMsgType.Init.value,
            'room_group_name': self.room_group_name,
            'channel_name': self.channel_name
        })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, data):
        print(type(data),data)
        if data['msg_type'] == ReceiveMsgType.SendThought.value:
            await writeThoughtAsync(data['data'])
            await self.send_json({
                'msg_type': SendMsgType.ReceiveThoughtSuccess.value,
                'data': data['data']
            })
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send.thought.group',
                    'channel_name': self.channel_name,
                    'data': data['data']
                }
            )
    async def send_thought_group(self,event):
        await self.send_json({
            'msg_type':SendMsgType.SendThoughtGroup.value,
            'channel_name':event['channel_name'],
            'data':event['data']
        })
