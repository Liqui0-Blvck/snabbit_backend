from django.db import models
from core.models import *
import random, string
from simple_history.models import HistoricalRecords as Historia
from .constantes_modelos import *
# Create your models here.

def codigo_equipo(length=6):
    return  ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

def ruta_imagen_equipo(instance, filename):
    return 'equipo/{0}/foto/{1}'.format(instance.nombre, filename)
  
def ruta_imagen_logo(instance, filename):
    return 'cliente/{0}/foto/{1}'.format(instance.nombre, filename)

class Clientes(ModeloBase):
  nombre = models.CharField(max_length=255)
  run = models.CharField(max_length=20)
  contacto = models.CharField(max_length=15, blank=True)
  correo = models.EmailField()
  tipo_cliente = models.CharField(max_length=1, choices=TIPO_CLIENTE, default='1')
  estado_cliente = models.CharField(max_length=100, blank=True)
  logo = models.ImageField(upload_to=ruta_imagen_logo)
  
  def __str__(self):
    return f"el cliente {self.nombre}"
  
  
class Usuario(ModeloBase):
  nombre = models.CharField(max_length=255)
  apellido = models.CharField(max_length=255, blank=True, null=True)
  correo = models.EmailField(max_length=100)
  departamento = models.CharField(max_length=255)
  cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)
  
  def __str__(self):
    return f"usuario {self.nombre}"
  
  
class Equipo(ModeloBase):
  marca = models.CharField(max_length=255) 
  codigo = models.CharField(max_length=6, default=codigo_equipo)
  procesador = models.CharField(max_length=255)
  detalle_procesador = models.CharField(max_length=255)
  ram = models.CharField(max_length=255)
  tipo_disco = models.CharField(max_length=255)
  capacidad_disco = models.CharField(max_length=255)
  licencia = models.CharField(max_length=255)
  numero_serie = models.CharField(max_length=255)
  foto = models.ImageField(upload_to=ruta_imagen_equipo, null=True, blank=True)
  fecha_compra = models.DateField(auto_now=True)
  registrado_por = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
  observaciones = models.TextField(blank=True, null=True)
  cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)
  
  usuarios = models.ManyToManyField(Usuario, through='clientes.EquipoUsuario')
  
  def __str__(self):
    return f"equipo {self.marca} {self.procesador}"
  
  
class EquipoUsuario(ModeloBase):
  usuario = models.ForeignKey('clientes.Usuario', on_delete=models.SET_NULL, null=True)
  equipo = models.ForeignKey('clientes.Equipo', on_delete=models.SET_NULL, null=True)
  activo = models.BooleanField(default=False)
  historia = Historia()
  
  def __str__(self):
    return f"equipo {self.equipo} del usuario {self.usuario}"
  
  class Meta:
    ordering = ['fecha_creacion']
  
class SolicitudTicket(ModeloBase):
  cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True)
  asunto = models.CharField(max_length=255, blank=True)
  descripcion = models.TextField()
  
  def __str__(self):
    return f"cliente {self.cliente}"

class Ticket(ModeloBase):
  cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True)
  tecnico = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
  prioridad = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='1')  
  titulo = models.CharField(max_length=150, blank=True)
  descripcion = models.TextField()
  estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='1')
  
  def __str__(self):
    return f"titulo {self.titulo}"
  
class Comentario(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    cuerpo = models.TextField()
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario en {self.ticket.titulo}'

class ArchivoAdjunto(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='archivos_adjuntos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='archivos_adjuntos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name

class RegistroActividad(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='registros_actividad', on_delete=models.CASCADE)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    actividad = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.actividad}'