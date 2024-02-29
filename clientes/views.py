from django.shortcuts import render
from rest_framework import filters, generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.

class ClienteListCreateAPIView(generics.ListCreateAPIView):
  queryset = Cliente.objects.all()
  serializer_class = ClientesSerializer
  
class ClienteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Cliente.objects.all()
  serializer_class = ClientesSerializer
  lookup_field = 'id'
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    
    self.perform_update(serializer)
    
    return Response(serializer.data)
  
  def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
         
         
     
class UsuarioListCreateAPIView(generics.ListCreateAPIView):
  search_fields = ['cliente__id']
  filter_backends = [filters.SearchFilter]
  queryset = Usuario.objects.all()
  serializer_class = UsuarioSerializer
   
class UsuarioUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Usuario.objects.all()
  serializer_class = UsuarioSerializer
  lookup_field = 'id'
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)
  
  def destroy(self, request, *args, **kwargs):
      usuarios_ids = request.data.get('ids', [])
      if not usuarios_ids:
          return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
      try:
          self.get_queryset().filter(id__in=usuarios_ids).delete()
          return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
      except Exception as e:
          return Response({'error': f'Error los usuarios: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
  