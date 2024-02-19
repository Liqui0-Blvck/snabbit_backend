from django.db import models
from core.models import ModeloBase
from .estados_modelo import ESTADO_OC

# Create your models here.

class OrdenDeCompra(ModeloBase):
  nombre = models.CharField(max_length=100)
  numero_oc = models.CharField(max_length=50)
  fecha_orden = models.DateField(blank=True, null=True)
  solicitado_por = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  estado_oc = models.CharField(max_length=1, choices=ESTADO_OC, default='1')
  proveedor = models.ForeignKey('items.Proveedor', on_delete=models.CASCADE)
  email_envia_oc = models.EmailField(max_length=100, blank=True, null=True)
  numero_cotizacion = models.CharField(max_length=100, blank=True, null=True)
  sucursal = models.ForeignKey('items.SucursalProveedor', on_delete=models.CASCADE, default=0)
  tranferido = models.BooleanField(default=False)

  
  items = models.ManyToManyField('items.Item', through='ordenes_de_compra.ItemOrdenDeCompra')
    
  class Meta:
    verbose_name_plural = 'ordenes_de_compra'
    
  def __str__(self):
    return self.nombre
  
  
class ItemOrdenDeCompra(ModeloBase):
  item = models.ForeignKey('items.Item', on_delete=models.CASCADE)
  orden_de_compra = models.ForeignKey('ordenes_de_compra.OrdenDeCompra', on_delete=models.CASCADE)
  unidad_de_compra = models.PositiveIntegerField(default=0)
  costo_por_unidad = models.IntegerField(default=0)
  fecha_llegada = models.DateTimeField(blank=True, null=True)
  observaciones = models.TextField(blank=True, null=True)
  
  class Meta:
    verbose_name_plural = 'items_orden_de_compra'
    
  def __str__(self):
    return '%s' %self.item
   