from django.contrib import admin
from .models import *
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.


@admin.register(StockItemBodega)
class StockEnBodegaAdmin(SimpleHistoryAdmin):
  list_display = ['id','item', 'cantidad',]
  history_list_display = ['cantidad']