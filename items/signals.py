from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

# @receiver(post_save, sender='ordenes_de_compra.OrdenDeCompra')
# def descarga_cantidad_a_stock_vincula_proveedor_en_item(sender, instance, created, **kwargs):
#   print(instance)
#   if instance.estado_oc == '5':
#     Stock
    
    # ProveedoresItem.objects.update_or_create(item = instance.items, proveedor = instance.proveedor)
    
@receiver(post_save, sender='items.Proveedor')
def creacion_casa_matriz(sender, instance, created, **kwargs):
    if created:
        SucursalProveedor.objects.create(
            proveedor=instance,
            direccion=instance.direccion,
            comuna = instance.comuna,
            region = instance.region,
            provincia = instance.provincia,
            nombre = 'Casa Matriz'
            )