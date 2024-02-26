from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(EquipoUsuario)
class EquipoUsuarioAdmin(admin.ModelAdmin):
  list_display = ['id', 'usuario', 'equipo']
  
@admin.register(Clientes)
class ClienteAdmin(admin.ModelAdmin):
  list_display = [id, 'nombre', 'tipo_cliente', 'estado_cliente']
    