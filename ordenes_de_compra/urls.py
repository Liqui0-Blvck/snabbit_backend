
from django.urls import path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
# router.register(r'orden-de-compra', OrdenDeCompraViewSet)
router.register(r'item-de-orden', ItemOrdenCompraViewset)


urlpatterns = [
  path('orden-compra/', OrdenesDeCompraAPIView.as_view(), name='orden-de-compra'),
  path('orden-compra/<int:pk_oc>', DetalleOrdenDeCompraAPIView.as_view(), name='detalle-orden-de-compra'),
  path('orden-compra-update/<int:id>', OrdenesDeCompraUpdateAPIView.as_view(), name='actualizar-estado-oc'),
  path('orden-compra-editar/<int:id>', OrdenDeCompraEditAPIView.as_view(), name='editar oc'),
  path('orden-compra-delete/', OrdenDeCompraEditAPIView.as_view(), name='editar oc')
]

urlpatterns += router.urls
