from django.shortcuts import render
from rest_framework import viewsets, filters, generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *


class ClienteListCreateAPIView(generics.ListCreateAPIView):
  
  queryset = Clientes.objects.all()
  serializer_class = ClientesSerializer
  
class ClienteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Clientes.objects.all()
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
      equipos_ids = request.data.get('ids', [])
      if not ordenes_ids:
          return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
      try:
          self.get_queryset().filter(id__in=ordenes_ids).delete()
          return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
      except Exception as e:
          return Response({'error': f'Error al eliminar items: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
  
  
class EquipoListCreateAPIView(generics.ListCreateAPIView):
  search_fields = ['cliente__id']
  filter_backends = [filters.SearchFilter]
  queryset = Equipo.objects.all()
  serializer_class = EquipoSerializer
  

class EquipoUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  search_fields = ['cliente__id']
  filter_backends = [filters.SearchFilter]
  queryset = Equipo.objects.all()
  serializer_class = EquipoSerializer
  lookup_field = 'id'
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)
  
  def destroy(self, request, *args, **kwargs):
    equipos_ids = request.data.get('ids', [])
    if not equipos_ids:
        return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        self.get_queryset().filter(id__in=equipos_ids).delete()
        return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error al eliminar items: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
  


class EquipoUsuarioListCreateAPIView(generics.ListCreateAPIView):
  search_fields = ['equipo__id']
  filter_backends = [filters.SearchFilter]
  queryset = EquipoUsuario.objects.all()
  serializer_class = EquipoUsuarioSerializer
  
  
class EquipoUsuarioUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = EquipoUsuario.objects.all()
  serializer_class = EquipoUsuarioSerializer
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


class EquipoUsuarioActivoUpdateAPIView(generics.UpdateAPIView):
  queryset = EquipoUsuario.objects.all()
  serializer_class = EquipoUsuarioSerializer
  lookup_field = 'id'
  
  def update(self, request, *args, **kwargs):
    equipo_usuario = EquipoUsuario.objects.get(pk = request.data)
    EquipoUsuario.objects.filter(equipo=equipo_usuario.equipo, activo=True).update(activo=False)

      # Activar el nuevo usuario
    equipo_usuario.activo = True
    equipo_usuario.save()

    return Response({"mensaje": "Usuario activado correctamente."}, status=status.HTTP_200_OK)

class SolicitudTicketListCreateAPIView(generics.ListCreateAPIView):
  queryset = SolicitudTicket.objects.all()
  serializer_class = SolicitudTicketSerializer
  

class TicketListAPIView(generics.ListAPIView):
  search_fields = ['cliente__id'] 
  filter_backends = [filters.SearchFilter]
  queryset = Ticket.objects.all()
  serializer_class = TicketSerializer

class TicketUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Ticket.objects.all()
  serializer_class = TicketSerializer
  lookup_field = 'id'
  
class TicketTecnicoUpdateAPIView(generics.UpdateAPIView):
  queryset = Ticket.objects.all()
  serializer_class = TicketTecnicoUpdate
  lookup_field = 'id'
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    
    self.perform_update(serializer)

    return Response(serializer.data)