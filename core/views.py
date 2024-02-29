from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import status

class PaginaInicio(TemplateView):
    template_name = 'core/pagina_inicio.html'


from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'viviendas': reverse('vivienda:lista-viviendas', request=request, format=format),
#         'invitaciones-integrantes': reverse('vivienda:lista-invitaciones', request=request, format=format),
        
      
#     })
    

from bd_ciudades.models import *
from .serializers import *

class ComunasList(generics.ListCreateAPIView):
    queryset = Comuna.objects.using('db_comunas').all()
    serializer_class = ComunasSerializer
    permission_classes = [IsAuthenticated,]
    
class RegionList(generics.ListCreateAPIView):
    queryset = Region.objects.using('db_comunas').all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated,]
    
    
class ProvinciaDetail(generics.RetrieveUpdateAPIView):
    queryset = Provincia.objects.using('db_comunas').all()
    serializer_class = ProvinciaSerializer
    permission_classes = [IsAuthenticated,]
    
class RegionDetail(generics.RetrieveUpdateAPIView):
    queryset = Region.objects.using('db_comunas').all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated,]
    
