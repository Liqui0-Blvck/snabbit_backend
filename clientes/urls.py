from django.urls import path
from .views import *

urlpatterns = [
    path('clientes/', ClienteListCreateAPIView.as_view()),
    path('cliente/<int:id>/', ClienteUpdateAPIView.as_view()),
    path('usuarios/', UsuarioListCreateAPIView.as_view()),
    path('usuario/<int:id>/', UsuarioUpdateDestroyAPIView.as_view()),
    path('usuario-delete/', UsuarioUpdateDestroyAPIView.as_view(    )),
    path('equipos/', EquipoListCreateAPIView.as_view()),
    path('equipo/<int:id>/', EquipoUpdateDestroyAPIView.as_view()),
    path('equipo-delete/', EquipoUpdateDestroyAPIView.as_view()),
    path('equipo-usuarios/', EquipoUsuarioListCreateAPIView.as_view()),
    path('equipo-usuario-update/<int:id>/', EquipoUsuarioActivoUpdateAPIView.as_view()),
    path('equipo-usuario/<int:id>/', EquipoUsuarioUpdateDestroyAPIView.as_view()),
    path('tickets/', TicketListAPIView.as_view()),
    path('ticket-up/', SolicitudTicketListCreateAPIView.as_view()),
    path('ticket/<int:id>/', TicketUpdateDeleteAPIView.as_view()),
    path('tecnico-ticket-update/<int:id>/', TicketTecnicoUpdateAPIView.as_view()),
    path('estado-ticket-update/<int:id>/', TicketEstadoUpdateAPIView.as_view()),
    
]
