from rest_framework import serializers
from .models import *
from comunas.models import *
from django.contrib.auth.models import User

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class PerfilSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    comuna_nombre = serializers.SerializerMethodField(read_only=True)
    provincia_nombre = serializers.SerializerMethodField(read_only=True)
    region_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Perfil
        fields = [
         'provincia',
         'region',
         'comuna',
         'provincia_nombre',
         'region_nombre',
         'comuna_nombre',
         'sobre_mi',
         'direccion',
         'cargo',
         'usuario',
         'foto',
         'contacto']

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

