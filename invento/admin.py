from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *
# Register your models here.


@admin.register(Invento)
class InventoAdmin(SimpleHistoryAdmin):
  list_display = ['id','nombre', ]
  history_list_display = ['id','nombre']
  
  