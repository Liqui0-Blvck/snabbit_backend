from django.urls import path
from .views import *



app_name = 'core'

urlpatterns = [
    # path('inicio/', PaginaInicio.as_view(), name='inicio'),
    # path('', api_root, name="apiroot"),
    path('core/tools/comunas', ComunasList.as_view(), name="lista_comunas"),
    path('core/tools/provincia/<int:pk>', ProvinciaDetail.as_view(), name="detalle_provincia"),
    path('core/tools/region', RegionList.as_view(), name="lista_regiones"),
    path('core/tools/region/<int:pk>', RegionDetail.as_view(), name="detalle_region"),

    
]
