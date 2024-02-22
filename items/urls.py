from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from .views import *


router = routers.SimpleRouter()
router.register(r'categoria', CategoriaViewSet)
router.register(r'proveedor'  , ProveedorViewSet )
router.register(r'sucursal', SucursalViewSet)

proveedores_router = routers.NestedSimpleRouter(router, r'proveedor', lookup='proveedor')
proveedores_router.register(r'sucursales', SucursalProveedorViewSet, basename='proveedor-sucursales')


urlpatterns = [
  path(r'', include(proveedores_router.urls)),
  path('items/', ItemListCreateAPIView.as_view(), name='list-and-create-items'),
  path('item/<int:id>/', ItemUpdateDestroyAPIView.as_view(), name='update-item'),
  path('item-delete/', ItemUpdateDestroyAPIView.as_view(), name='delete-many-items'),
  
]

urlpatterns += router.urls  
