from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import *
from .serializers import *

# Create your views here.

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    
    
    
class UserRegisterAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistroSerializer
    
    
class TecnicosAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = TecnicoSerializer
    
    