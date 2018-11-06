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
        We should be able to serialize an asset:
            Create the expected dict representation.
        """
        asset = Asset(description="fake asset", original_cost=9999999999.99)
        asset.save()
        
        loc1 = Location(description='loc1')
        loc1.save()
        
        loc2 = Location(description='loc2')
        loc2.save()
        
        Count(asset=asset, location=loc1, count=25).save()
        Count(asset=asset, location=loc2, count=30).save()
        serializer = AssetSerializer(asset)
        
        expected = {'id': 1, 
            'description': 'fake asset', 
            'original_cost': '9999999999.99',
            'locations': 
                [{'location':'loc1', 'count':25}, 
                 {'location':'loc2', 'count':30}]}
        
        self.assertDictEqual(serializer.data, expected)
        
        
    def test_asset_can_be_deserialized(self):
        """Deserialize an asset that has been correctly serialized:"""
        
        """1. serialize asset (convert to raw python data structure)"""
        asset = Asset(description="fake asset", original_cost=9999999999.99)
        asset.save()
        serializer = AssetSerializer(asset)
        asset = None
        
        """2. convert to json string"""
        content = JSONRenderer().render(serializer.data)
        
        """3. convert from json string back to raw python data structure"""
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = AssetSerializer(data=data)
        serializer.is_valid()
        
        """4. convert this data structure to Asset object instance"""
        asset = serializer.save()

      
class LocationSerializerTest(TestCase):
    
    def test_location_can_be_serialized(self):
        """Serialize a location."""
        location = Location(description="fake location")
        location.save()
        serializer = LocationSerializer(location)
        self.assertDictEqual(serializer.data, 
                             {'id': 1, 'description': 'fake location'})
        
    def test_location_can_be_deserialized(self):
        """Deserialize a location that has been correctly serialized:"""
        
        """1. serialize location (convert to raw python data structure)"""
        location = Location(description="fake location")
        location.save()
        serializer = LocationSerializer(location)
        location = None
        
        """2. convert to json string"""
        content = JSONRenderer().render(serializer.data)
        
        """3. convert from json string back to raw python data structure"""
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = LocationSerializer(data=data)
        serializer.is_valid()
        
        """4. convert this data structure to Location object instance"""
        location = serializer.save()
        
        