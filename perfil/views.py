from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import *
from .models import *
from .serializers import *
from comunas.models import *
from django.shortcuts import get_object_or_404
# Create your views here.

class PerfilViewSet(viewsets.ModelViewSet):
  queryset = Perfil.objects.all()
  serializer_class = PerfilSerializer
  
  def create(self, request, *args, **kwargs):
    data = request.data
    
    region_id = data.get('region')
    
    provincias = Provincia.objects.using("db_comunas").filter(provincia_region=region_id)
    provincia_id = None
    comuna_id = None

    # Obtener provincia_id
    for provincia in provincias.values():
      if provincia['provincia_id'] == data.get('provincia'):
          provincia_id = provincia['provincia_id']
          break
    
    comunas = Comuna.objects.using("db_comunas").filter(comuna_provincia=provincia_id)
    # Obtener comuna_id
    for comuna in comunas.values():
      if comuna['comuna_id'] == data.get('comuna'):
          comuna_id = comuna['comuna_id']
          break
      
    print(f'\n {provincia_id} \n {region_id} \n {comuna_id}')
    
    perfil_data = {
      'usuario': data.get('usuario'),
      'provincia': provincia_id,
      'comuna': comuna_id,
      'region': region_id,
      'sobre_mi': data.get('sobre_mi'),
      'direccion': data.get('direccion'),
      'cargo': data.get('cargo'),
    }
    perfil_serializer = PerfilSerializer(data=perfil_data)
    print('\n',perfil_serializer, '\n')
    
    if perfil_serializer.is_valid():
      perfil_serializer.save()
      return Response({'message': 'Perfil creado exitosamente'})
    else:
      return Response({'error': perfil_serializer.errors })
      