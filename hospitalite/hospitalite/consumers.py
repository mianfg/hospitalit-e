import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import *


class MatchConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connect", event)

        await self.send({
            "type" : "websocket.accept"
        })

        await asyncio.sleep(10)
        await self.send({
            "type" : "websocket.send",
            "text" : "Hello world"
        })

        """
        if ( usuario es voluntario ):
            insertar usuario en cola
        else:
            esperar a voluntario
            cuando encuentra voluntario:
                enviar mensaje de usuario encontrado
        
        """
    
    async def websocket_receive(self, event):
        print("receive", event)
    
    async def websocket_disconnect(self, event):
        print("disconnect", event)

    @database_sync_to_async
    def add_user_to_queue(self, username, type):
        pass

    #@database_sync_to_async
    