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
    if obj.content_type.id == 13:
      serializer = ItemSerializer(instance = item, many=True)
      item_data_dict = {}
      for objeto in serializer.data:
          item_data_dict['id'] = objeto['id']
          item_data_dict['nombre'] = objeto['nombre'] 
      return [item_data_dict]
    
    elif obj.content_type.id == 31:
      serializer = InventoSerializer(instance = invento, many=True)
      invento_data_dict = {}
      for objeto in serializer.data:
        invento_data_dict[objeto['id']] = objeto['nombre']
      return [item_data_dict]

    
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
      instance.save()

      return instance


class ContentTypeItemsEnGuia(serializers.ModelSerializer):
  class Meta:
    model = ContentType
    fields = '__all__'