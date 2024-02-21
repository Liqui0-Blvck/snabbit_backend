from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from items.models import *
from invento.models import *
import json

# Create your views here.

class GuiaSalidaUpdateAPIView(generics.UpdateAPIView):
    queryset = GuiaDeSalida.objects.all()
    serializer_class = GuiaSalidaPutSerializer
    lookup_field = 'id'
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance, data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        self.perform_update(serializer)

        return Response(serializer.data)

class GuiaDeSalidaListCreateAPIView(generics.ListCreateAPIView):
  queryset = GuiaDeSalida.objects.all()
  serializer_class = GuiaSalidaSerializer
  
  def create(self, request, *args, **kwargs):
      # Serializar los datos recibidos para la guía de salida
      guia_serializer = self.get_serializer(data=request.data)
      if guia_serializer.is_valid():
          # Guardar la guía de salida
          guia_salida = guia_serializer.save()

          # Serializar y guardar los objetos en la guía de salida
          objetos_guia = request.POST.get('objetos_en_guia', '[]')
          objetos = json.loads(objetos_guia)
          for objeto_data in objetos:
              # Asignar la guía de salida al objeto
              
              objeto_data['guia_salida'] = guia_salida.pk
              objeto_serializer = ItemEnGuiaSerializer(data=objeto_data)
              if objeto_serializer.is_valid():
                  objeto_serializer.save()
              else:
                  # Si hay algún error en la validación del objeto, eliminar la guía de salida y retornar los errores
                  guia_salida.delete()
                  return Response(objeto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
          # Retornar la guía de salida creada junto con los objetos asociados
          return Response(guia_serializer.data, status=status.HTTP_201_CREATED)
      else:
          # Si hay algún error en la validación de la guía de salida, retornar los errores
          return Response(guia_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GuiaDeSalidaUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = GuiaDeSalida.objects.all()
  serializer_class = GuiaSalidaSerializer
  lookup_field = 'id'
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data = request.data)
    
    if serializer.is_valid():
      objetos_guia = request.POST.get('objetos_en_guia', '[]')
      objetos = json.loads(objetos_guia)

      for objeto in objetos:
        objeto_id = objeto.get('id')

        
        try:
          objeto_existe = ItemsEnGuia.objects.get(id=objeto_id)
          nuevo_objeto_id = objeto.get('id')
          if objeto_existe.content_type == 13:
            nuevo_item = Item.objects.get(id=nuevo_objeto_id)
            objeto_existe.object_id = nuevo_item
          elif objeto_existe.content_type == 31:
            nuevo_invento = Invento.objects.get(id=nuevo_objeto_id)
            objeto_existe.object_id = nuevo_invento
          objeto_existe.cantidad = objeto.get('cantidad')
          objeto_existe.save()
            
        except ItemsEnGuia.DoesNotExist:
          objeto['guia_salida'] = instance.pk
          objeto_serializer = ItemEnGuiaSerializer(data = objeto)
          
          if objeto_serializer.is_valid():
            objeto_serializer.save()
          else:
            return Response(objeto_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
  def destroy(self, request, *args, **kwargs):
    guias_ids = request.data.get('ids', [])
    if not guias_ids:
        return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        self.get_queryset().filter(id__in=guias_ids).delete()
        return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error al eliminar items: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemEnGuiaListCreateAPIView(generics.ListCreateAPIView):
  queryset = ItemsEnGuia.objects.all()
  serializer_class = ItemEnGuiaSerializer
