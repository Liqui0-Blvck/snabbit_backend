from django.contrib import admin
from .models import *
from import_export.admin import *
# Register your models here.

class ItemOCInline(admin.TabularInline):
  model = ItemOrdenDeCompra
  
  
@admin.register(OrdenDeCompra)
class OrdenDeCompraAdmin(ImportExportModelAdmin):
  list_display = ['nombre', 'numero_oc', 'fecha_orden']
  inlines = [ItemOCInline, ]
  
  

