from rest_framework import serializers
from .models import *
from items.models import *
from bodega.models import *

class ItemEnInventoSerializer(serializers.ModelSerializer):
  item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
  item_nombre = serializers.SerializerMethodField()
  class Meta:
    model = ItemEnInvento
    fields = '__all__'
    
  def get_item_nombre(self, obj):
    return obj.item.nombre if obj.item else None

class InventoSerializer(serializers.ModelSerializer):
  items = ItemEnInventoSerializer(read_only=True, many=True, required=False, source='itemeninvento_set')
  stock_bodega = serializers.SerializerMethodField(read_only=True)
  
  class Meta:
    model = Invento
    fields = '__all__'
    
  def get_stock_bodega(self, obj):
        try:
            stock = StockInventoBodega.objects.get(invento = obj)
            return stock.cantidad
        except: 
            return str('sin stock')
    
