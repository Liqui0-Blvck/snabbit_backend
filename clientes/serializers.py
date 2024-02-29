from rest_framework import serializers
from .models import *


class UsuarioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Usuario
    fields = '__all__'


class ClientesSerializer(serializers.ModelSerializer):
  usuarios = UsuarioSerializer(many=True, read_only=True, source='usuario_set')
  tipo_cliente_label = serializers.SerializerMethodField()

  class Meta:
    model = Cliente
    fields = '__all__'
    
  def get_tipo_cliente_label(self, obj):
    return obj.get_tipo_cliente_display()
  
  
