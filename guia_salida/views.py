from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from items.models import *
from invento.models import *
# Create your views here.

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
          objetos_en_guia_data = request.data.pop('objetos_en_guia', [])  # Extraer datos de los objetos en la guía
          for objeto_data in objetos_en_guia_data:
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
      objetos_guia = request.data.get('objetos_en_guia', [])
      print(objetos_guia)
      for objeto in objetos_guia:
        objeto_id = objeto.get('id')
        print(objeto_id)
        
        
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
    
  
class ItemEnGuiaListCreateAPIView(generics.ListCreateAPIView):
  queryset = ItemsEnGuia.objects.all()
  serializer_class = ItemEnGuiaSerializer