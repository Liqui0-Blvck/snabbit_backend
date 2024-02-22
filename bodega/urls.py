from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
# router.register(r'contenedor', ContenedorViewSet)
# router.register(r'items_contenedor', ItemEnContenedorViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('contenedores/', ContenedorListCreateAPIView.as_view(), name='list-create-contenedores'),
  path('contenedor/<int:id>/', ContenedorUpdateDestroyAPIView.as_view(), name='update-contenedor'),
  path('contenedores-delete/', ContenedorUpdateDestroyAPIView.as_view(), name='delete-many-contenedores'),
  path('historia/<int:pk>', HistorialAPIView.as_view(), name='historia-stock-items')
]
