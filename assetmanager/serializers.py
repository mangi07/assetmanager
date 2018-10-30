# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Asset, Location, Count

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

