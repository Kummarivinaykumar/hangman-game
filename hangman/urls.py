from django.urls import path
from .views import start_game, reset_game

urlpatterns = [
    path('', start_game, name='start_game'),
    path('reset/', reset_game, name='reset_game'),
]