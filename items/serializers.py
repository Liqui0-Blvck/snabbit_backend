from rest_framework import serializers
from .models import *
from bodega.models import *
from comunas.models import *
from simple_history.models import *

class SucursalSerializer(serializers.ModelSerializer):
    proveedor = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all())
    comuna_nombre = serializers.SerializerMethodField(read_only=True)
    provincia_nombre = serializers.SerializerMethodField(read_only=True)
    region_nombre = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = SucursalProveedor
        fields = '__all__'
        
    def get_comuna_nombre(self, obj):
        comuna_id = obj.comuna
        comuna = Comuna.objects.using("db_comunas").filter(comuna_id=comuna_id).first()
        return comuna.comuna_nombre if comuna else None

    def get_provincia_nombre(self, obj):
        provincia_id = obj.provincia
        provincia = Provincia.objects.using("db_comunas").filter(provincia_id=provincia_id).first()
        return provincia.provincia_nombre if provincia else None

    def get_region_nombre(self, obj):
        region_id = obj.region
        region = Region.objects.using("db_comunas").filter(region_id=region_id).first()
        return region.region_nombre if region else None 
    
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    sucursales = SucursalSerializer(many=True, read_only=True, source='sucursalproveedor_set')
    comuna_nombre = serializers.SerializerMethodField(read_only=True)
    provincia_nombre = serializers.SerializerMethodField(read_only=True)
    region_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Proveedor
        fields = '__all__'
    
    def get_comuna_nombre(self, obj):
        comuna_id = obj.comuna
        comuna = Comuna.objects.using("db_comunas").filter(comuna_id=comuna_id).first()
        return comuna.comuna_nombre if comuna else None

    def get_provincia_nombre(self, obj):
        provincia_id = obj.provincia
        provincia = Provincia.objects.using("db_comunas").filter(provincia_id=provincia_id).first()
        return provincia.provincia_nombre if provincia else None

    def get_region_nombre(self, obj):
        region_id = obj.region
        region = Region.objects.using("db_comunas").filter(region_id=region_id).first()
        return region.region_nombre if region else None
    
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.rut = validated_data.get('rut', instance.rut)
        instance.correo = validated_data.get('correo', instance.correo)
        instance.contacto = validated_data.get('contacto', instance.contacto)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.comuna = validated_data.get('comuna', instance.comuna)
        instance.region = validated_data.get('region', instance.region)
        instance.provincia = validated_data.get('provincia', instance.provincia)
        
        foto = validated_data.get('foto')
        if foto:
            instance.foto = foto

        instance.save()
        return instance
        
class ProveedoresItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProveedoresItem
        fields = '__all__'
    
class ItemSerializer(serializers.ModelSerializer):
    proveedores = ProveedorSerializer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = '__all__'
        

class ItemListSerializer(serializers.ModelSerializer):
    # proveedores = ProveedorSerializer(many=True, read_only=True)
    stock_bodega = serializers.SerializerMethodField()
    nombre_categoria = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = '__all__'
        
    def get_nombre_categoria(self, instance):
        return instance.categoria.nombre if instance.categoria else None
    
    def get_stock_bodega(self, obj):
        try:
            stock = StockItemBodega.objects.get(item = obj)
            return stock.cantidad
        except: 
            return str('sin stock')