from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *
from items.models import *

@receiver(post_save, sender='items.Item')
def vincula_item_a_stock_bodega(sender, instance, created, **kwargs):
  if created and instance:
    StockItemBodega.objects.update_or_create(item = instance)
    
@receiver(post_save, sender='invento.Invento')
def traspaso_invento_stockenbodega(sender, created, instance, **kwargs):
  if created and instance:
    StockInventoBodega.objects.update_or_create(invento = instance, cantidad = 1)
    
    
@receiver(post_save, sender='ordenes_de_compra.OrdenDeCompra')
def transpasa_cantidad_a_stockenbodega(sender, instance, **kwargs):
  if instance.estado_oc == '5':
    for item in instance.itemordendecompra_set.all():
      stock_item = StockItemBodega.objects.get(item = item.item.pk)
      previo_stock = stock_item.cantidad
      nuevo_stock = stock_item.cantidad + item.unidad_de_compra
      stock_item.cantidad = nuevo_stock
      stock_item._change_reason = f'{item.item.nombre} ha aumentado su cantidad de {previo_stock} a {nuevo_stock} segun OC {instance.pk}'
      stock_item.save()
      it = Item.objects.get(pk = item.item.pk)
      prov = Proveedor.objects.get(pk = instance.proveedor.pk)
      ProveedoresItem.objects.update_or_create(item = it, proveedor = prov, orden_de_compra = instance)


  
    

# @receiver(post_save, sender='ordenes_de_compra.OrdenDeCompra')
# def descuento_cantidad_a_stockenbodega(sender, instance, **kwargs):
#   # print(instance.itemordendecompra_set.all())
#   if instance.estado_oc == '5':
#     for item in instance.itemordendecompra_set.all():
#       print(item.item.pk)
#       stock_item = StockItemBodega.objects.get(item = item.item.pk)
#       previo_stock = stock_item.cantidad
#       nuevo_stock = stock_item.cantidad - item.unidad_de_compra
#       stock_item.cantidad = nuevo_stock
#       stock_item._change_reason = f'{item.item.nombre} ha disminuido su cantidad de {previo_stock} a {nuevo_stock} segun OC {instance.pk}'
#       stock_item.save()
#       it = Item.objects.get(pk = item.item.pk)
#       prov = Proveedor.objects.get(pk = instance.proveedor.pk)
#       ProveedoresItem.objects.update_or_create(item = it, proveedor = prov, orden_de_compra = instance)
    