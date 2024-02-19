from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bodega.urls')),
    path('api/', include('items.urls')),
    # path('', include('items.urls')),
    path('api/', include('ordenes_de_compra.urls')),
    path('api/', include('perfil.urls')),
    path('api/', include('comunas.urls')),
    path('api/', include('clientes.urls')),
    path('api/', include('invento.urls')),
    path('api/', include('guia_salida.urls')),
    path('auth/', include('auth_custom.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)