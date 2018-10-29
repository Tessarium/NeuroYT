from django.shortcuts import render
from .models import Recognise
from .serializers import RecogniseSerializer
from rest_framework import generics
# Create your views here.


class RecogniseListCreate(generics.ListCreateAPIView):
    queryset = Recognise.objects.all()
    serializer_class = RecogniseSerializer
