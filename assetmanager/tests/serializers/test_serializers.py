# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

from ...models import Asset, Location, Count
from ...serializers import AssetSerializer, LocationSerializer

class AssetSerializerTest(TestCase):
    
    def test_asset_can_be_serialized(self):
        """
        We should be able to serialize an asset.
        """
        asset = Asset(description="fake asset")
        asset.save()
        serializer = AssetSerializer(asset)
        # print(serializer.data)
        # example: {'id': 1, 'description': 'fake asset'}
        
    def test_asset_can_be_deserialized(self):
        """
        We should be able to deserialize an asset that has been correctly serialized:
        1. serialize asset (convert to raw python data structure)
        2. convert to json string
        3. convert from json string back to raw python data structure
        4. convert this data structure to Asset object instance
        """
        # 1
        asset = Asset(description="fake asset")
        asset.save()
        serializer = AssetSerializer(asset)
        asset = None
        
        # 2
        content = JSONRenderer().render(serializer.data)
        # print("content")
        # print(content)
        # b'{"id":1,"description":"fake asset"}'
        
        # 3
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        # print("data")
        # print(data)
        # {'id': 1, 'description': 'fake asset'}
        serializer = AssetSerializer(data=data)
        serializer.is_valid()
        # True
        # print(repr(serializer))
        # print(serializer.validated_data)
        # OrderedDict([('description', 'fake asset')])
        
        # 4
        asset = serializer.save()
        # print("asset")
        # print(asset)
        # fake asset
      
class LocationSerializerTest(TestCase):
    
    def test_location_can_be_serialized(self):
        """
        We should be able to serialize a location.
        """
        location = Location(description="fake location")
        location.save()
        
        serializer = LocationSerializer(location)
        # print(serializer.data)
        # example: {'id': 1, 'description': 'fake location'}
        
    def test_location_can_be_deserialized(self):
        """
        We should be able to deserialize an asset that has been correctly serialized:
        1. serialize asset (convert to raw python data structure)
        2. convert to json string
        3. convert from json string back to raw python data structure
        4. convert this data structure to Asset object instance
        """
        # 1
        location = Location(description="fake location")
        location.save()
        serializer = LocationSerializer(location)
        location = None
        
        # 2
        content = JSONRenderer().render(serializer.data)
        # print("content")
        # print(content)
        # b'{"id":1,"description":"fake location"}'
        
        # 3
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        # print("data")
        # print(data)
        # {'id': 1, 'description': 'fake location'}
        serializer = LocationSerializer(data=data)
        serializer.is_valid()
        # True
        # print("serializer.validated_data")
        # print(serializer.validated_data)
        # OrderedDict([('description', 'fake location')])
        
        # 4
        location = serializer.save()
        # print("location")
        # print(location)
        # fake location