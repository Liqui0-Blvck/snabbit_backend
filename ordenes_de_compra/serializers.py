from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from items.serializers import *


class ItemOrdenDeCompraSerializer(serializers.ModelSerializer):
  item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
  item_nombre = serializers.SerializerMethodField()

  class Meta:
    model = ItemOrdenDeCompra
    fields = '__all__'

  def get_item_nombre(self, instance):
    return instance.item.nombre if instance.item else None


class OrdenDeCompraSerializer(serializers.ModelSerializer):
  solicitado_por = serializers.StringRelatedField(read_only=True)
  proveedor_nombre = serializers.SerializerMethodField()
  estado_oc_label = serializers.SerializerMethodField()
  items = ItemOrdenDeCompraSerializer(many=True, required=False, read_only=True, source='itemordendecompra_set')
  # proveedor = ProveedorSerializer(read_only=True)
  sucursal_nombre = serializers.SerializerMethodField()
  
  class Meta:
    model = OrdenDeCompra
    exclude = ['estado_oc']
    
  def get_proveedor_nombre(self, instance):
    return instance.proveedor.nombre if instance.proveedor else None
    
  def get_estado_oc_label(self, obj):
    return obj.get_estado_oc_display()
  
  def get_sucursal_nombre(self, instance):
    return instance.sucursal.nombre if instance.sucursal else None
  
  
class OrdenDeCompraPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenDeCompra
        fields = ['estado_oc', 'tranferido']

    def update(self, instance, validated_data):
      instance.estado_oc = validated_data.get('estado_oc', instance.estado_oc)

      if instance.estado_oc == '5':
        instance.tranferido = True
      instance.save()

      return instance

