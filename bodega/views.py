from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView

# Create your views here.
class ContenedorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Contenedor.objects.all()
    serializer_class = ContenedorSerializer

class ContenedorUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contenedor.objects.all()
    serializer_class = ContenedorSerializer
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        contenedores_ids = request.data.get('ids', [])
        if not contenedores_ids:
            return Response({'Error': 'No se han proporcionado ids valido'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.get_queryset().filter(id__in=contenedores_ids).delete()
            return Response({'Success': 'Contenedores eliminados exitosamente!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Error': 'Error al eliminar los contenedores'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ItemEnContenedorViewSet(viewsets.ModelViewSet):
    queryset = ItemEnContenedor.objects.all()
    serializer_class = ItemEnContenedorSerializer
    # permission_classes = [permissions.IsAuthenticated]    

class HistorialAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        objeto = StockItemBodega.objects.get(item=pk)
        historial = objeto.historia.all()
        serializer = HistorialSerializer(historial, many=True)
        return Response(serializer.data)