import json
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.models import Q
# Create your views here.

class InventoListCreateAPIView(generics.ListCreateAPIView):
  queryset = Invento.objects.all()
  serializer_class = InventoSerializer
  
  def create(self, request, *args, **kwargs):
      items_json = request.POST.get('items', '[]')
      items = json.loads(items_json)

      serializer = self.get_serializer(data=request.data)

      if serializer.is_valid():
          invento = serializer.save()

          for item_data in items:
              item_data['invento'] = invento.id
              item_serializer = ItemEnInventoSerializer(data=item_data)
              if item_serializer.is_valid():
                  item_serializer.save()
              else:
                  return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

          return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Invento.objects.all()
  serializer_class = InventoSerializer
  lookup_field = 'id'
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data)

    if serializer.is_valid():
        items_json = request.data.get('items', '[]')
        items = json.loads(items_json)
        item_ids_in_request = [item.get('id') for item in items]
        item_existentes_ids = list(instance.itemeninvento_set.values_list('id', flat=True))
        items_to_delete_ids = set(item_existentes_ids) - set(item_ids_in_request)
        ItemEnInvento.objects.filter(id__in=items_to_delete_ids).delete()
        for item in items:
            item_id = item.get('id')
            nuevo_item_id = item.get('item')
            cantidad = item.get('cantidad')
            

            try:
                item_existente = ItemEnInvento.objects.get(pk=item_id)
                if instance.itemeninvento_set.filter(id=item_existente.id).exists():
                    # Si el elemento existente está asociado con el objeto de inventario
                    nuevo_item = Item.objects.get(id=nuevo_item_id)
                    
                    # Actualizar el elemento existente
                    item_existente.item = nuevo_item
                    item_existente.cantidad = cantidad
                    item_existente.save()
            except ItemEnInvento.DoesNotExist:
                # Crear un nuevo item si no existe
                item['invento'] = instance.pk
                item_serializer = ItemEnInventoSerializer(data=item)

                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, *args, **kwargs):
    invento_ids = request.data.get('ids', [])
    if not invento_ids:
        return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        self.get_queryset().filter(id__in=invento_ids).delete()
        return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error al eliminar items: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
      