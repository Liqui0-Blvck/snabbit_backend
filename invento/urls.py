from django.urls import path
from .views import *

urlpatterns = [
    path('inventos/', InventoListAPIView.as_view()),
    path('invento/', InventoUpdateDestroyAPIView.as_view()), 
    path('invento/<int:id>/', InventoUpdateDestroyAPIView.as_view()),
    
]
