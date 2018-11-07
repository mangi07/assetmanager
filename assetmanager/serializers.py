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

    def save_locations(self, asset, locations):
        for location in locations:
            description = location['location']
            count = location['count']
            # TODO: return error to user if location does not exist (and test this)
            
            loc = Location.objects.filter(description=description).first()
            # TODO: use update if count exists (and test this)
            
            
            Count.objects.create(asset=asset, location=loc, count=count)
            
    def create(self, validated_data):
        location_data = validated_data.pop('locations')
        asset = Asset.objects.create(**validated_data)
        self.save_locations(asset, location_data)
        return asset
    
    def update(self, asset, validated_data):
        if validated_data['locations']:
            location_data = validated_data.pop('locations')
            self.save_locations(asset, location_data)
        asset.description = validated_data.get('description', asset.description)
        asset.original_cost = validated_data.get('original_cost', asset.original_cost)
        # TODO: is there a way to iterate through these mappings so 
        # this does not have to be changed when the model expands
        asset.save()
        return asset
