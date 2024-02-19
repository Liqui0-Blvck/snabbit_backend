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
  path('items/', ItemListCreateAPIView.as_view()),
  path('item/<int:id>/', ItemUpdateDestroyAPIView.as_view()),
  path('item/', ItemUpdateDestroyAPIView.as_view()),
  
]

urlpatterns += router.urls  
