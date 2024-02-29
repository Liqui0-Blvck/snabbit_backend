from django.urls import path
from .views import *

urlpatterns = [
    path('clientes/', ClienteListCreateAPIView.as_view(), name='list-create-clientes'),
    path('cliente/<int:id>/', ClienteUpdateAPIView.as_view(), name='update-delete-cliente'),
    path('usuarios/', UsuarioListCreateAPIView.as_view()),
    path('usuario/<int:id>/', UsuarioUpdateDestroyAPIView.as_view()),
    path('usuario-delete/', UsuarioUpdateDestroyAPIView.as_view()),
]
