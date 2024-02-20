from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import *
from .estados_modelos import *
# Create your models here.

def ruta_imagen_firma(instance, filename):
  return 'guia_salida/firmas/{0}/foto/{1}'.format(instance.destinatario, filename)

class GuiaDeSalida(ModeloBase):
  destinatario = models.CharField(max_length=255)
  direccion = models.CharField(max_length=255, blank=True)
  encargado = models.CharField(max_length=255, blank=True, null=True)
  numero_guia = models.CharField(max_length=100, blank=True)
  nombre_receptor = models.CharField(max_length=255, blank=True, null=True)
  estado_guia = models.CharField(max_length=1, choices=ESTADO_GUIA, default='1')
  foto_firma = models.ImageField(upload_to=ruta_imagen_firma, blank=True)
  
  def __str__(self):
    return f"guia {self.numero_guia}"
  
class ItemsEnGuia(ModeloBase):
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  guia_salida = models.ForeignKey(GuiaDeSalida, on_delete=models.CASCADE)
  cantidad = models.IntegerField(default=0)