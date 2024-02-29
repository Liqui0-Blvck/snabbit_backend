from rest_framework import serializers
from bd_ciudades.models import *
from rest_framework import serializers



class ComunasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'



