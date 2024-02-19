from rest_framework import serializers
from .models import *
from simple_history.models import *
from items.serializers import *

class ContenedorSerializer(serializers.ModelSerializer):
    items = ItemSerializer(read_only=True, many=True)
    class Meta:
        model = Contenedor
        fields = '__all__'
        
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.color = validated_data.get('color', instance.color)
        instance.dimensiones = validated_data.get('dimensiones', instance.dimensiones)
        instance.material = validated_data.get('material', instance.material)
        instance.estado = validated_data.get('estado', instance.estado)
        
        # Verificar si se proporciona una nueva foto
        foto = validated_data.get('foto')
        if foto:
            instance.foto = foto

        instance.save()
        return instance
    
class ItemEnContenedorSerializer(serializers.ModelSerializer):
    nombre_item = serializers.SerializerMethodField()
    nombre_contenedor = serializers.SerializerMethodField()
    class Meta:
        model = ItemEnContenedor
        fields = '__all__'
        # exclude = ['stock_bodega']
        
    def get_nombre_item(self, instance):
        return instance.item.nombre if instance.item else None
    
    def get_nombre_contenedor(self, instance):
        return instance.contenedor.nombre if instance.contenedor else None
    
class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItemBodega.historia.model  # Accede al modelo de historial
        fields = '__all__' 