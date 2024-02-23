from rest_framework import serializers
from .models import *

class ClientesSerializer(serializers.ModelSerializer):
  tipo_cliente_label = serializers.SerializerMethodField()

  class Meta:
    model = Clientes
    fields = '__all__'
    
  def get_tipo_cliente_label(self, obj):
    return obj.get_tipo_cliente_display()
  

class UsuarioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Usuario
    fields = '__all__'

class EquipoUsuarioSerializer(serializers.ModelSerializer):
  usuario_nombre = serializers.SerializerMethodField()
  usuario_departamento = serializers.SerializerMethodField()  
  class Meta:
      model = EquipoUsuario
      fields = '__all__'
  
  def get_usuario_nombre(self, obj):
    return obj.usuario.nombre if obj.usuario else None
  
  def get_usuario_departamento(self, obj):
    return obj.usuario.departamento if obj.usuario else None

class EquipoUsuarioActiveSerializer(serializers.ModelSerializer):
  class Meta:
    model = EquipoUsuario
    fields = ['activo']
    
class EquipoSerializer(serializers.ModelSerializer):
  usuarios = EquipoUsuarioSerializer(many=True, read_only=True, required=False, source='equipousuario_set')
  class Meta:
    model = Equipo
    exclude = ['foto']
  

class TicketSerializer(serializers.ModelSerializer):
  nombre_cliente = serializers.SerializerMethodField()
  nombre_tecnico = serializers.SerializerMethodField()
  prioridad_display = serializers.SerializerMethodField()
  estado_display = serializers.SerializerMethodField()
  
  class Meta:
    model = Ticket
    fields = '__all__'
    
  def get_prioridad_display(self, obj):
    return obj.get_prioridad_display()

  def get_estado_display(self, obj):
    return obj.get_estado_display()
  
  def get_nombre_tecnico(self, obj):
    return obj.tecnico.username if obj.tecnico else None
    
  def get_nombre_cliente(self, obj):
    return obj.cliente.nombre if obj.cliente else None
  
class TicketTecnicoUpdate(serializers.ModelSerializer):
  class Meta:
    model = Ticket
    fields = ['tecnico']
    
  def update(self, instance, validated_data):
      instance.tecnico = validated_data.get('tecnico', instance.tecnico)
      instance.save()
      return instance
    
class TicketEstadoUpdate(serializers.ModelSerializer):
  class Meta:
    model = Ticket
    fields = ['estado']
    
  def update(self, instance, validated_data):
    print(instance.estado)
    instance.estado = validated_data.get('estado', instance.estado)
    instance.save()
    return instance

    
class SolicitudTicketSerializer(serializers.ModelSerializer):
  class Meta:
    model = SolicitudTicket
    fields = '__all__'