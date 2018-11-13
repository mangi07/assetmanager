# -*- coding: utf-8 -*-

from rest_framework import serializers
from .custom_api_exceptions import BadRequestException
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
            # TODO: test this or change it
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
        internal_value.update({
            "locations": locations
        })
        return internal_value

    def find_unique_descs(self, descs):
        while(len(descs) > 0):
            desc = descs.pop()
            if desc in descs:
                return desc
        return None
        
    def save_locations(self, asset, locations):
        """A list of counts per location is given for the asset.
        If the there is already a count of the asset at a given location,
        it will be updated.  Otherwise, the given location count will
        be newly associated with the asset."""
        
        # fail if duplicate locations are given
        descs = [loc['location'] for loc in locations]
        dup_descr = self.find_unique_descs(descs)
        if dup_descr:
            raise BadRequestException(
                ("Duplicate locations given: '{}'".format(dup_descr))
            )
        
        for location in locations:
            descr = location['location']
            count = location['count']
            # this filter returns None if location description not found
            loc = Location.objects.filter(description=descr).first()
            if not loc:
                raise BadRequestException(
                        ("'{}' location does not exist."  
                         "  You need to first create the location before "
                         "trying to add an asset count to it.".format(descr))
                    )
                        
            # update count if it exists, otherwise create it
            location_count = Count.objects.filter(asset=asset, location=loc).first()
            if location_count:
                location_count.count = count
                location_count.save()
                #Count.objects.update(location=loc, count=count)
            else:
                Count.objects.create(asset=asset, location=loc, count=count)
            
    def create(self, validated_data):
        location_data = validated_data.pop('locations')
        asset = Asset.objects.create(**validated_data)
        try:
            self.save_locations(asset, location_data)
        except BadRequestException:
            asset.delete()
            raise
        return asset
    
    
    def update(self, asset, validated_data):
        if validated_data['locations']:
            location_data = validated_data.pop('locations')
            self.save_locations(asset, location_data)
        asset.description = validated_data.get('description', asset.description)
        asset.original_cost = validated_data.get('original_cost', asset.original_cost)
        # TODO: is there a way to iterate through these mappings so 
        # this does not have to be changed when the model expands?
        asset.save()
        return asset
