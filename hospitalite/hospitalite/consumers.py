import asyncio
import json
import uuid
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from .models import *


class MatchConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.current_user = self.scope['user']
        self.is_voluntario = await self.is_voluntario(self.current_user)
        self.group = await self.get_group(self.current_user)

        # aceptar conexión WebSocket
        await self.send({
            "type" : "websocket.accept"
        })

        # añadir a un grupo propio (comunicación uno-a-uno)
        await self.channel_layer.group_add(
            'group-'+self.current_user.username,
            self.channel_name
        )
        # añadir a su grupo (comunicación uno-a-muchos)
        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        message = {
            "type"  : "connect",
            "group" : self.group,
            "username"  : self.current_user.username
        }

        await self.send({
            "type" : "websocket.send",
            "text" : json.dumps(message)
        })
    
    async def websocket_receive(self, event):
        print("receive", event)
        message = json.loads(event['text'])
        message_type = message['type']
        
        if message_type == 'rating':
            print("GOT RATING")
            await self.add_rating(message)

        if message_type == 'do_queue':
            message = {
                "type" : "queued"
            }

            await self.send({
                "type" : "websocket.send",
                "text" : json.dumps(message)
            })

            if not self.is_voluntario:
                await self.remove_user_from_queue(self.current_user)
                await self.add_user_to_queue(self.current_user)

                message = {
                    "type" : "new_no_voluntario"
                }

                print("ENVIANDO MENSAJE A VLUNTARIOS")

                await self.channel_layer.group_send(
                    'voluntario',
                    {
                        "type" : "send_message",
                        "text" : json.dumps(message)
                    }
                )
        if message_type == 'check_matches':
            match_user, match = await self.get_user_from_queue()
            unique = str(uuid.uuid1()).replace("-", "")

            if match:   # si hay un match
                match_username = match_user.username
                data = await self.get_user_serialized(match_username)
                data['uuid'] = unique
                data['match_id'] = match.id

                message = {
                    "type" : "match",
                    "info" : json.dumps(data)
                }

                await self.send({
                    "type" : "websocket.send",
                    "text" : json.dumps(message)
                })

                data = await self.get_user_serialized(self.current_user.username)
                data['uuid'] = unique
                data['match_id'] = match.id

                message = {
                    "type" : "match",
                    "info" : json.dumps(data)
                }
                await self.channel_layer.group_send(
                    'group-'+match_username,
                    {
                        "type" : "send_message",
                        "text" : json.dumps(message)
                    }
                )



    async def send_message(self, event):
        await self.send({
            "type" : "websocket.send",
            "text" : event['text']
        })
    
    async def websocket_disconnect(self, event):
        # eliminar no voluntario de cola
        if not self.is_voluntario:
            await self.remove_user_from_queue(self.current_user)

    @database_sync_to_async
    def is_voluntario(self, user):
        return user.is_voluntario()
    
    @database_sync_to_async
    def get_group(self, user):
        return user.get_group()
    
    @database_sync_to_async
    def add_user_to_queue(self, user):
        q = MatchingQueue(username=user)
        q.save()
    
    @database_sync_to_async
    def get_user_from_queue(self):
        # WIP aquí se implementa el criterio de selección
        # se puede pasar como parámetro el voluntario para ponderar
        # en este caso se ordena por timestamp y se pilla el enfermo
        # que ha entrado antes
        
        if MatchingQueue.objects.all():
            q = MatchingQueue.objects.earliest('timestamp')
            user = q.username
            m = Match(
                username1=self.current_user,
                username2=user
            )
            m.save()
            q.delete()
        else:
            user = None
            m = None
        
        return user, m
    
    @database_sync_to_async
    def remove_user_from_queue(self, user):
        MatchingQueue.objects.filter(username=user).delete()
    
    @database_sync_to_async
    def get_user_serialized(self, username):
        u = Usuario.objects.filter(username=username)[0]
        return u.serialize()
    
    @database_sync_to_async
    def add_rating(self, message):
        r = Rating(
            id_match=Match.objects.get(id=message['match_id']),
            from_user=Usuario.objects.get(username=message['from']),
            rating=message['rating'],
            comentario=message['comment']
        )
        r.save()