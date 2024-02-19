from django.urls import path
from .views import *

urlpatterns = [
    path('guia_salidas/', GuiaDeSalidaListCreateAPIView.as_view()),
    path("guia_salida/<int:id>/", GuiaDeSalidaUpdateDestroyAPIView.as_view(), name=""),
    path('item_guia/', ItemEnGuiaListCreateAPIView.as_view())
]
