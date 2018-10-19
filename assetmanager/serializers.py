# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Asset, Location, Count

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ('id', 'description')
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'description', 'assets')

