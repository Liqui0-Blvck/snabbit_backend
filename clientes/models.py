from django.db import models
from core.models import *
from .constantes_modelos import *



# Create your models here.

def ruta_imagen_logo(instance, filename):
    return 'cliente/{0}/foto/{1}'.format(instance.nombre, filename)
  
class Cliente(ModeloBase):
  nombre = models.CharField(max_length=255)
  run = models.CharField(max_length=20)
  contacto = models.CharField(max_length=15, blank=True)
  correo = models.EmailField()
  tipo_cliente = models.CharField(max_length=1, choices=TIPO_CLIENTE, default='1')
  estado_cliente = models.CharField(max_length=100, blank=True)
  logo = models.ImageField(upload_to=ruta_imagen_logo, blank=True, null=True)
  
  usuarios = models.ManyToManyField('self', through='clientes.Usuario')
  
  class Meta:
    verbose_name = "cliente"
    verbose_name_plural = "clientes"
  
  def __str__(self):
    return f"el cliente {self.nombre}"
  
  
class Usuario(ModeloBase):
  nombre = models.CharField(max_length=255)
  apellido = models.CharField(max_length=255, blank=True, null=True)
  correo = models.EmailField(max_length=100)
  departamento = models.CharField(max_length=255)
  cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
  
  def __str__(self):
    return f"usuario {self.nombre}"