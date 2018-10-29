from django.urls import path
from . import views


urlpatterns = [
    path('api/recognise/', views.RecogniseListCreate.as_view()),
]
