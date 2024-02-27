from django.urls import path
from .views import *

urlpatterns = [
    path('guia_salidas/', GuiaDeSalidaListCreateAPIView.as_view()),
    path("guia_salida/<int:id>/", GuiaDeSalidaUpdateDestroyAPIView.as_view(), name=""),
    path('guia_salida_update/<int:id>', GuiaSalidaUpdateAPIView.as_view(), name='actualizar-estado-guia'),
    path("guia_salida_delete/", GuiaDeSalidaUpdateDestroyAPIView.as_view(), name=""),
    path('item_guia/', ItemEnGuiaListCreateAPIView.as_view()),
    path('content-types/', ContentTypesItemsEnGuiaAPIView.as_view())
]
    