from django.db import models
from core.models import ModeloBase
from django.contrib.auth.models import User
# Create your models here.

def ruta_imagen(instance, filename):
  return 'perfil/{0}/foto/{1}'.format(instance.usuario.first_name, filename)


class Perfil(ModeloBase):
  usuario = models.OneToOneField(User, on_delete=models.CASCADE)
  provincia = models.IntegerField(default=0, blank=True)
  region = models.IntegerField(default=0, blank=True)
  comuna = models.IntegerField(default=0, blank=True)
  foto = models.ImageField(upload_to=ruta_imagen, blank=True)
  sobre_mi = models.TextField(max_length=255, blank=True, null=True)
  direccion = models.CharField(max_length=255, blank=True, null=True)
  cargo = models.CharField(max_length=255, blank=True, null=True)
  contacto = models.CharField(max_length=12, blank=True, null=True)
  
  class Meta:
    verbose_name = 'perfil'
    verbose_name_plural = 'perfiles'
  
  def __str__(self):
    return f'{self.usuario}'
  