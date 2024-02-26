from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *
from items.models import *
from django.contrib.contenttypes.models import *
from items.models import *
from invento.models import *

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
      
      
@receiver(post_save, sender='guia_salida.GuiaDeSalida')
def transpasa_cantidad_a_stockenbodega(sender, instance, **kwargs):
  stock_objeto = None
  objeto_nombre = None
  ct_invento = ContentType.objects.get_for_model(Invento)
  ct_item = ContentType.objects.get_for_model(Item)
  
  
  if instance.estado_guia == '5':
    for obj in instance.itemsenguia_set.all():
      print(obj.content_type.model)
      # if obj.content_type == ct_item:
      #   stock_objeto = StockItemBodega.objects.get(item = obj.object_id)
      #   objeto_nombre = stock_objeto.item.nombre
        
      # elif obj.content_type == ct_invento:
      #   stock_objeto = StockInventoBodega.objects.get(invento = obj.object_id)
      #   objeto_nombre = stock_objeto.invento.nombre  
      # previo_stock = stock_objeto.cantidad
      # nuevo_stock = stock_objeto.cantidad - obj.cantidad
      # stock_objeto.cantidad = nuevo_stock
      # stock_objeto._change_reason = f'{objeto_nombre} ha descendio su cantidad de {previo_stock} a {nuevo_stock} segun Guia de Salida {instance.pk}'
      # stock_objeto.save()
      
         
      

  
    

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
    