# -*- coding: utf-8 -*-

from rest_framework import serializers
from .custom_api_exceptions import BadRequestException
from .models import Asset, Location, Count
from django.db import transaction
from abc import ABC, abstractmethod
from .tests.schemas.utils import load_json_schema
from jsonschema import validate
from . import serializer_utils


class CustomUpdateSerializer(ABC):
    """Handles a list of DB entries to be updated via either patch or put request"""
    @abstractmethod
    def _validate_post_data(self):
        """should raise an exception if data is invalid"""
        # may want to validate differently depending on
        # whether this serializer is called by a post or a patch
        pass
    
    @abstractmethod
    def _assign_item_fields(self, loc, update_locs, id):
        """should assign values from dict update_locs to corresponding properties of loc"""
        pass
    
    def __init__(self, model, serializer, data=None, many=False):
        self.data=data
        self.many=many
        self.items=None
        self.errors=""
        self.Serializer = serializer
        self.Model = model
    
    def validate_post_data(self):
        if not self.data:
            raise BadRequestException("Post data missing.")
        try:
            # each item of data list should have a proper key 'id'
            assert type(self.data) == list
            for d in self.data:
                assert "id" in d
                int(d["id"])
            # custom validations in child class
            self._validate_post_data()
        except:
            raise BadRequestException("Post data format is incorrect.")
    
    def is_valid(self):
        self.validate_post_data()
        id_list = [item['id'] for item in self.data]
        items = self.Model.objects.filter(pk__in=id_list)
        if items and len(items) == len(id_list):
            self.items = items
            return True
        self.errors = "One or more items were not found. No updates performed."
        return False
    
    @transaction.atomic
    def save(self):
        if not self.items:
            raise RuntimeError("save called before is_valid")
        # make dictionary out of data
        update_items = {}
        for d in self.data:
             update_items[int(d['id'])] = d
        for item in self.items:
            update_item = update_items[item.id]
            self._assign_item_fields(item, update_item)
            item.save()
        id_list = list(update_items.keys())
        items = self.Model.objects.filter(pk__in=id_list)
        self.data = self.Serializer(items, many=True).data


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        #fields = '__all__'
        fields = ('id', 'description', 'created', 'in_location', 'location_nesting')
        
        
class LocationUpdateSerializer(CustomUpdateSerializer):
    """updates a list of locations"""
    def __init__(self, data=None, many=False):
        super().__init__(Location, LocationSerializer, data, many)
        
    def _validate_post_data(self):
        """should raise an exception if data is invalid"""
        for loc in self.data:
             int(loc['id'])
             str(loc['description'])
             if 'in_location' in loc:
                 int(loc['in_location'])
    
    def _assign_item_fields(self, loc, update_loc):
            loc.description = update_loc['description']
            if 'in_location' in update_loc:
                loc.in_location = int(loc['in_location'])

# TODO: this was being used but might go away
#class LocationField(serializers.RelatedField):
#    def to_representation(self, value):
#        try:
#            # value passed in is location object,
#            # so need to get count object here, instead
#            count = Count.objects.get(pk=value.id).count
#        except:
#            # TODO: test this or change it
#            count = 0
#            print(value)
#        return {'location':value.description, 'count':count}

    
class AssetSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField()
    
    class Meta:
        model = Asset
        fields = ('id', 'description','original_cost','locations','created')
    
    def get_locations(self, asset):
        counts_per_location = []
        try:
            # value passed in is asset object,
            # so need to get count object here, instead
            count_objs = Count.objects.filter(asset=asset.id)
            for count_obj in count_objs:
                location = Location.objects.get(pk=count_obj.location.id)
                count = {'location':location.location_nesting, 'count':count_obj.count}
                counts_per_location.append(count)
        except:
            raise BadRequestException("Error retrieving location counts in AssetSerializer.")
        return counts_per_location
    
    def to_internal_value(self, data):
        internal_value = super(AssetSerializer, self).to_internal_value(data)
        locations = data.get("locations")
        internal_value.update({
            "locations": locations
        })
        return internal_value

    def find_duplicate_descs(self, descs):
        while(len(descs) > 0):
            desc = descs.pop()
            if desc in descs:
                return desc
        return None
    
            
    def create(self, validated_data):
        location_data = validated_data.pop('locations')
        asset = Asset.objects.create(**validated_data)
        try:
            serializer_utils.save_asset_locations(asset, location_data)
        except BadRequestException:
            asset.delete()
            raise
        return asset
    
    
    def update(self, asset, validated_data):
        # TODO: refactor out this to use serializer_utils.update_asset
        if validated_data['locations']:
            location_data = validated_data.pop('locations')
            serializer_utils.save_asset_locations(asset, location_data)
        asset.description = validated_data.get('description', asset.description)
        asset.original_cost = validated_data.get('original_cost', asset.original_cost)
        # TODO: is there a way to iterate through these mappings so
        # this does not have to be changed when the model expands?
        asset.save()
        return asset

class AssetUpdateSerializer(CustomUpdateSerializer):
    """
    updates a list of assets
    """
    def __init__(self, data=None, many=False):
        super().__init__(Asset, AssetSerializer, data, many)
        
    def _validate_post_data(self):
        """should raise an exception if data is invalid"""
        json_schema = load_json_schema("asset_patch.json")
        validate(self.data, json_schema)
    
    def _assign_item_fields(self, asset, update_asset):
        if 'locations' in update_asset:
            location_data = update_asset.pop('locations')
            serializer_utils.save_asset_locations(asset, location_data)
        serializer_utils.assign_asset_fields(asset, update_asset)
        
            
