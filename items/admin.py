from django.contrib import admin
from .models import *
from import_export.admin import *
# Register your models here.
class ProveedorOCInline(admin.TabularInline):
  model = Proveedor
  
  
# @admin.register(SucursalProveedor)
# class SucursalAdmin(admin.ModelAdmin):
#   list_display = ['direccion', 'numero']
#   inlines = [ProveedorOCInline, ]
  
  
# admin.site.register(Item)
class ProveedoresInLine(admin.TabularInline):
  model = ProveedoresItem
  
  
@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
  list_display = ['pk', 'nombre', 'fecha_creacion' ]
  inlines = [ProveedoresInLine, ]


@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
  list_display = ['pk', 'nombre']
  
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
  list_display = ['pk', 'nombre', 'fecha_creacion' ]