from django.urls import path
from .views import *

urlpatterns = [
    path('inventos/', InventoListCreateAPIView.as_view(), name='list-create-inventos'),
    path('invento/<int:id>/', InventoUpdateDestroyAPIView.as_view(), name='update-invento'),
    path('inventos-delete/', InventoUpdateDestroyAPIView.as_view(), name='delete-many-inventos'),

]
