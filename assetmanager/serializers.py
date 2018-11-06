# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Asset, Location, Count

        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationField(serializers.RelatedField):
    def to_representation(self, value):
        try:
            count = Count.objects.get(pk=value.id).count
        except:
            count = 0
        return {'location':value.description, 'count':count}
    
class AssetSerializer(serializers.ModelSerializer):
    locations = LocationField(many=True, read_only=True)
    
    class Meta:
        model = Asset
        fields = ('id', 'description','original_cost','locations')
    
    def to_internal_value(self, data):
        internal_value = super(AssetSerializer, self).to_internal_value(data)
        locations = data.get("locations")
        #my_non_model_field_value = ConvertRawValueInSomeCleverWay(my_non_model_field_raw_value)
        internal_value.update({
            "locations": locations
        })
        return internal_value

    def create(self, validated_data):
        location_data = validated_data.pop('locations')
        print(location_data)
        asset = Asset.objects.create(**validated_data)
        for location in location_data:
            description = location['location']
            count = location['count']
            loc = Location.objects.filter(description=description).first()
            Count.objects.create(asset=asset, location=loc, count=count)
        return asset
