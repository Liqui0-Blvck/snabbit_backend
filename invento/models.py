from django.db import models
from core.models import *
# Create your models here.
from simple_history.models import HistoricalRecords


def ruta_imagen(instance, filename):
  return 'invento/{0}/foto/{1}'.format(instance.nombre, filename)


class Invento(ModeloBase):
  nombre = models.CharField(max_length=255, blank=True)
  descripcion = models.TextField(blank=True, null=True)
  foto = models.ImageField(upload_to=ruta_imagen, blank=True, null=True)
  items = models.ManyToManyField('items.Item', through='ItemEnInvento')
  historia = HistoricalRecords(
    history_change_reason_field=models.TextField(null=True)
  )
  def __str__(self):
    return f'invento {self.nombre}'
  
class ItemEnInvento(ModeloBase):
  item = models.ForeignKey('items.Item', on_delete=models.SET_NULL, null=True)
  invento = models.ForeignKey('invento.Invento', on_delete=models.SET_NULL, null=True)
  cantidad = models.IntegerField(default=0)

  def __str__(self):
    return f'invento {self.item}'