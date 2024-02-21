from django.contrib import admin
from .models import *
from simple_history.admin import *
# Register your models here.


@admin.register(GuiaDeSalida)
class GuiaDeSalidaAdmin(SimpleHistoryAdmin):
  list_display = ['id','encargado', ]
  history_list_display = ['id','encargado']