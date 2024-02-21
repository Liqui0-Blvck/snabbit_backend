from rest_framework import serializers
from .models import *
from items.serializers import *
from invento.serializers import *

class ItemEnGuiaSerializer(serializers.ModelSerializer):
  articulo = serializers.SerializerMethodField()
  class Meta:
    model = ItemsEnGuia
    fields = '__all__'
    
  def get_articulo(self, obj):
    item = Item.objects.filter(id=obj.object_id)
    invento = Invento.objects.filter(id=obj.object_id)
    if obj.content_type.model == 'item':
      serializer = ItemSerializer(instance = item, many=True)
      return serializer.data
    elif obj.content_type.model == 'invento':
      serializer = InventoSerializer(instance = invento, many=True)
      return serializer.data

    
class GuiaSalidaSerializer(serializers.ModelSerializer):
  objetos_en_guia = serializers.SerializerMethodField()
  estado_guia_label = serializers.SerializerMethodField()
  class Meta:
    model = GuiaDeSalida
    fields = '__all__'
  
  def get_estado_guia_label(self, obj):
    return obj.get_estado_guia_display()
  
  def get_objetos_en_guia(self, obj):
    articulo = ItemsEnGuia.objects.filter(guia_salida=obj)
    serializer = ItemEnGuiaSerializer(instance=articulo, many=True)
    return serializer.data
  
  
class GuiaSalidaPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaDeSalida
        fields = ['estado_guia']

    def update(self, instance, validated_data):
      instance.estado_guia = validated_data.get('estado_guia', instance.estado_guia )

      # if instance.estado_oc == '5':
      #   instance.tranferido = True
      instance.save()

      return instance
