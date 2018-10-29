from django.core import serializers
from .models import Recognise
from .serializers import RecogniseSerializer

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class Consumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = 'detectors'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_recognise(self, *args):
        # data = serializers.serialize('json', Recognise.objects.all(), fields=('counter_cars',
        #                                                                       'created'))
        recs = Recognise.objects.all()
        data = []
        for rec in recs:
            data.append({
                'id': rec.pk,
                'counter_cars': rec.counter_cars,
                'created': str(rec.created)
            })

        self.send(text_data=json.dumps(data))
