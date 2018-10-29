from rest_framework import serializers
from .models import Recognise


class RecogniseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recognise
        fields = ('id', 'counter_cars', 'created')
