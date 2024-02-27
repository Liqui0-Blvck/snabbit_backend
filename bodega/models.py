from django.db import models
from simple_history.models import HistoricalRecords as Historia
from core.models import ModeloBase
import random, string


def codigo_contenedor(length=6):
    return  ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))
# Create your models here.}

def ruta_imagen(instance, filename):
    return 'contenedor/{0}/foto/{1}'.format(instance.nombre, filename)


class Contenedor(ModeloBase):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=6, blank=True, null=True)
    color = models.CharField(max_length=100, blank=True, null=True)
    dimensiones = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True)
    items = models.ManyToManyField('items.Item', through='bodega.ItemEnContenedor')
    foto = models.ImageField(upload_to=ruta_imagen, blank=True, null=True)
    historia = Historia()
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = codigo_contenedor()
        super(Contenedor, self).save(*args, **kwargs)
    
    
class StockItemBodega(ModeloBase):
    cantidad = models.PositiveIntegerField(default=0)
    item = models.OneToOneField('items.Item', on_delete=models.CASCADE)
    historia = Historia(
        history_change_reason_field = models.TextField(null=True)
    )
    
    def __str__(self):
        return f'{self.item}'
    
class StockInventoBodega(ModeloBase):
    cantidad = models.PositiveIntegerField(default=0)
    invento = models.OneToOneField('invento.Invento', on_delete=models.CASCADE)
    historia = Historia(
        history_change_reason_field = models.TextField(null=True)
    )
    

class ItemEnContenedor(ModeloBase):
    item = models.ForeignKey('items.Item', on_delete = models.CASCADE)
    contenedor = models.ForeignKey(Contenedor, on_delete = models.CASCADE)
    # stock_bodega = models.ForeignKey(StockItemBodega, on_delete=models.CASCADE)
    
    

    
    