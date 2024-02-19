from rest_framework import viewsets, generics, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q


class OrdenesDeCompraUpdateAPIView(generics.UpdateAPIView):
    queryset = OrdenDeCompra.objects.all()
    serializer_class = OrdenDeCompraPutSerializer
    lookup_field = 'id'
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(instance, data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        self.perform_update(serializer)

        return Response(serializer.data)
    
class OrdenDeCompraEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrdenDeCompra.objects.all()
    serializer_class = OrdenDeCompraSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        
        if serializer.is_valid():
            items = request.data.get('items', [])
            print(items)
            
            for item_data in items:
                item_id = item_data.get('id')
                
                print("\n veremos el id", item_id)
                try:
                    item_existente = ItemOrdenDeCompra.objects.get(pk=item_id)
                    
                    print("que es esto", item_existente)
                    
                    if instance.itemordendecompra_set.filter(id=item_existente.id).exists():
                        print("dentro del loop", item_existente)
                        nuevo_item_id = item_data.get('item')
                        nuevo_item = Item.objects.get(id=nuevo_item_id)
                        
                        # # Resto del código para actualizar el item existente...
                        item_existente.item = nuevo_item
                        item_existente.unidad_de_compra = item_data.get('unidad_de_compra', item_existente.unidad_de_compra)
                        item_existente.costo_por_unidad = item_data.get('costo_por_unidad', item_existente.costo_por_unidad)
                        item_existente.fecha_llegada = item_data.get('fecha_llegada', item_existente.fecha_llegada)
                        item_existente.observaciones = item_data.get('observaciones', item_existente.observaciones)
                        item_existente.save()

                        print(f"Item {item_id} actualizado correctamente")
                    else:
                        print("ctm la huea pesa")
                        pregunta = instance.itemordendecompra_set.filter(~Q(id = item_existente.id)).delete()
                        print("soy el que te devuelve los queryset", pregunta)
                except ItemOrdenDeCompra.DoesNotExist:
                    item_data['orden_de_compra'] = instance.pk
                    item_serializer = ItemOrdenDeCompraSerializer(data=item_data)   
                    
                    if item_serializer.is_valid():
                        item_serializer.save()
                        print(f"Item {item_id} creado correctamente")
                    else:
                        print(f"No se pudo crear el nuevo item {item_id}: {item_serializer.errors}")
            
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        ordenes_ids = request.data.get('ids', [])
        if not ordenes_ids:
            return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.get_queryset().filter(id__in=ordenes_ids).delete()
            return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al eliminar items: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class OrdenesDeCompraAPIView(generics.ListCreateAPIView):
    queryset = OrdenDeCompra.objects.all()
    serializer_class = OrdenDeCompraSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    
    def create(self, request, *args, **kwargs):
        items_data = request.data.get('items', [])
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            orden_de_compra = serializer.save(solicitado_por=self.request.user)
            
            for item_data in items_data:
                item_data['orden_de_compra'] = orden_de_compra.id
                item_serializer = ItemOrdenDeCompraSerializer(data=item_data)
                
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
class DetalleOrdenDeCompraAPIView(generics.RetrieveUpdateAPIView):
    queryset = OrdenDeCompra.objects.all()
    serializer_class = OrdenDeCompraSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        oc = get_object_or_404(queryset, pk = self.kwargs['pk_oc'])
        self.check_object_permissions(self.request, oc)
        return oc
    
class ItemOrdenCompraViewset(viewsets.ModelViewSet):
    queryset = ItemOrdenDeCompra.objects.all()
    serializer_class = ItemOrdenDeCompraSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Deserializar los datos recibidos en la solicitud
        
        # print("item orden Consulta", request.data)
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        print("serializador consultado", serializer)
        serializer.is_valid(raise_exception=True)

        # Guardar los items de orden en la base de datos
        self.perform_create(serializer)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
        
    
        
    
        
   
      
        


