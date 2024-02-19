from django.db import models
from core.models import *
# Create your models here.
from simple_history.models import HistoricalRecords


def ruta_imagen(instance, filename):
  return 'invento/{0}/foto/{1}'.format(instance.nombre, filename)

class CustomHistoricalRecords(HistoricalRecords):
    """
    Custom HistoricalRecords class with change_reason as TextField.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history_change_reason = models.TextField()

class Invento(ModeloBase):
  nombre = models.CharField(max_length=255, blank=True)
  descripcion = models.TextField(blank=True, null=True)
  foto = models.ImageField(upload_to=ruta_imagen, blank=True, null=True)
  items = models.ManyToManyField('items.Item', through='ItemEnInvento')
  historia = CustomHistoricalRecords()
  def __str__(self):
    return f'invento {self.nombre}'
  
class ItemEnInvento(ModeloBase):
  item = models.ForeignKey('items.Item', on_delete=models.SET_NULL, null=True)
  invento = models.ForeignKey('invento.Invento', on_delete=models.SET_NULL, null=True)
  cantidad = models.IntegerField(default=0)

  def __str__(self):
    return f'invento {self.item}'