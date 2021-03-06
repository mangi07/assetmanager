# -*- coding: utf-8 -*-

from rest_framework import serializers
from .custom_api_exceptions import BadRequestException
from .models import Asset, Location, Count
from django.db import transaction
from abc import ABC, abstractmethod
from .tests.schemas.utils import load_json_schema
from jsonschema import validate
from . import serializer_utils
from . import permissions


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
    
    def __init__(self, user, model, serializer, data=None, many=False):
        self.user = user
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
        
        item_ids = list(items.values_list('id', flat=True))
        difference = set(id_list).difference(item_ids)
        if items and len(items) == len(id_list):
            self.items = items
            return True
        self.errors = "No updates performed because items with the following ids were not found: " + str(difference) + "."
        return False
    
    @transaction.atomic
    def save(self):
        if not self.items:
            raise RuntimeError("save called before is_valid")
        # make dictionary out of data
        if not permissions.can_update_items(self.Model, self.data, self.user):
            raise BadRequestException("You do not have permission to perform this save operation.")
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

# TODO: need to validate outside db level to prevent duplicate descriptions with no parent locations
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        #fields = '__all__'
        fields = ('id', 'description', 'created', 'in_location', 'location_nesting')
        
        
class LocationUpdateSerializer(CustomUpdateSerializer):
    """updates a list of locations"""
    def __init__(self, user, data=None, many=False):
        super().__init__(user, Location, LocationSerializer, data, many)
    
    # TODO: Need to test this!!
    def _validate_post_data(self):
        """should raise an exception if data is invalid"""
        for loc in self.data:
            int(loc['id'])
            assert('description' in loc or 'in_location' in loc)
            if 'description' in loc:
                str(loc['description'])
            if 'in_location' in loc and loc['in_location'] is not None:
                int(loc['in_location'])
    
    # TODO: Need to add this to unit tests!! - only tested informally in django browsable api
    def _assign_item_fields(self, loc, update_loc):
        if 'description' in update_loc:
            loc.description = update_loc['description']
        if 'in_location' in update_loc:
            if update_loc['in_location'] is None:
                loc.in_location = update_loc['in_location']
                return
            in_location = Location.objects.filter(
                pk=int(update_loc['in_location'])
            ).first()
            if in_location is None:
                raise BadRequestException("Could not find location with id " + update_loc['in_location'] + ".")
            loc.in_location = in_location

    
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
                count = {'id':location.id, 'location':location.location_nesting, 'count':count_obj.count}
                counts_per_location.append(count)
        except:
            raise BadRequestException("Error retrieving location counts in AssetSerializer.")
        return counts_per_location
    
    # TODO (authorization): override the to_representation method to determine which fields a user may view
    # TODO (authorization): see https://www.django-rest-framework.org/api-guide/serializers/#overriding-serialization-and-deserialization-behavior
    def to_representation(self, asset):
        ret = super().to_representation(asset)
        # TODO (authorization): filter allowed values based on permissions
        return ret
    
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
        # TODO (authorization): check that user has permissions to save in permissions.py
        location_data = validated_data.pop('locations')
        asset = Asset.objects.create(**validated_data)
        try:
            serializer_utils.save_asset_locations(asset, location_data)
        except BadRequestException:
            asset.delete()
            raise
        return asset
    
    
    def update(self, asset, validated_data):
        # TODO (authorization): check that user has permissions to save in permissions.py
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
    def __init__(self, user, data=None, many=False):
        super().__init__(user, Asset, AssetSerializer, data, many)
        
    def _validate_post_data(self):
        """should raise an exception if data is invalid"""
        json_schema = load_json_schema("asset_patch.json")
        validate(self.data, json_schema)
    
    def _assign_item_fields(self, asset, update_asset):
        if 'locations' in update_asset:
            location_data = update_asset.pop('locations')
            serializer_utils.save_asset_locations(asset, location_data)
        serializer_utils.assign_asset_fields(asset, update_asset)
        
            
