# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Asset, Location, Count

        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationField(serializers.RelatedField):
    def to_representation(self, value):
        return {value.description, value.count}
    
class AssetSerializer(serializers.ModelSerializer):
    locations = LocationField(many=True, read_only=True)
    
    class Meta:
        model = Asset
        fields = ('id', 'description','original_cost','locations')
