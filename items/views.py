from django.shortcuts import render
from rest_framework import viewsets, filters, generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        items_ids = request.data.get('ids', [])
        if not items_ids:
            return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.get_queryset().filter(id__in=items_ids).delete()
            return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al eliminar items: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
            
    def destroy(self, request, *args, **kwargs):
        items_ids = request.data.get('ids', [])
        if not items_ids:
            return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.get_queryset().filter(id__in=items_ids).delete()
            return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error al eliminar items: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

 
class SucursalProveedorViewSet(viewsets.ModelViewSet):
    queryset = SucursalProveedor.objects.all()
    serializer_class = SucursalSerializer
    
    def get_queryset(self):
        print(self.kwargs)
        proveedor_id = self.kwargs['proveedor_pk']
        return SucursalProveedor.objects.filter(proveedor=proveedor_id)
    
class SucursalViewSet(viewsets.ModelViewSet):
    queryset = SucursalProveedor.objects.all()
    serializer_class = SucursalSerializer
    search_fields = ['proveedor__id']
    filter_backends = (filters.SearchFilter, )
    # permission_classes = [permissions.IsAuthenticated]


class ItemListCreateAPIView(generics.ListCreateAPIView):    
  search_fields = ['nombre']
  filter_backends = (filters.SearchFilter, )
  queryset = Item.objects.all()
  serializer_class = ItemListSerializer

class ItemUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Item.objects.all()
  serializer_class = ItemSerializer
  lookup_field = 'id'
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance, data = request.data, partial = True)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, *args, **kwargs):
    items_ids = request.data.get('ids', [])
    if not items_ids:
        return Response({'error' : 'no se proporcionaron ids validos'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        self.get_queryset().filter(id__in=items_ids).delete()
        return Response({'success': 'Elimando con exito'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error al eliminar items: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
      