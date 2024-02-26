from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import *
from .estados_modelos import *
from simple_history.models import HistoricalRecords 
# Create your models here.
import random, string

def codigo_contenedor(length=6):
    return  ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

def ruta_imagen_firma(instance, filename):
  return 'guia_salida/firmas/{0}/foto/{1}'.format(instance.destinatario, filename)

class GuiaDeSalida(ModeloBase):
  destinatario = models.CharField(max_length=255)
  direccion = models.CharField(max_length=255, blank=True)
  encargado = models.CharField(max_length=255, blank=True, null=True)
  numero_guia = models.CharField(max_length=100, blank=True)
  nombre_receptor = models.CharField(max_length=255, blank=True, null=True)
  estado_guia = models.CharField(max_length=1, choices=ESTADO_GUIA, default='1')
  firma_encargado = models.ImageField(upload_to=ruta_imagen_firma, blank=True)
  firma_recepcion = models.ImageField(upload_to=ruta_imagen_firma, blank=True)
  elementos = models.ManyToManyField('self', through='guia_salida.ItemsEnGuia')
  historia = HistoricalRecords(
    history_change_reason_field = models.TextField(null=True)
  )
  
  def __str__(self):
    return f"guia {self.numero_guia}"
  
  def save(self, *args, **kwargs):
    if not self.numero_guia:
        self.numero_guia = codigo_contenedor()
    super(GuiaDeSalida, self).save(*args, **kwargs)
  
class ItemsEnGuia(ModeloBase):
  opciones = models.Q(app_label = 'item', model = 'item') | models.Q(app_label = 'invento', model = 'invento')
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=opciones)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  guia_salida = models.ForeignKey(GuiaDeSalida, on_delete=models.CASCADE)
  cantidad = models.IntegerField(default=0)