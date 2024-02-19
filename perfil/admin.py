from django.contrib import admin
from .models import *
from comunas.models import *
# Register your models here.


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
  list_display = ['usuario', 'fecha_creacion']