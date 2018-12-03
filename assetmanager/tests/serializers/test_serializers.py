# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

from ...models import Asset, Location, Count
from ...serializers import AssetSerializer, LocationSerializer, LocationUpdateSerializer
from ...custom_api_exceptions import BadRequestException
from ..schemas.utils import load_json_schema

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
        data = {'id': 1, 'description': 'fake location1'}
        
        """3. convert from json string back to raw python data structure"""
        content = JSONRenderer().render(data)
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = LocationSerializer(data=data)
        serializer.is_valid()
        
        """4. convert this data structure to Location object instance"""
        location = serializer.save()
        
        self.assertEqual(location.description, 'fake location1')
        
        
    def test_location_descriptions_must_be_unique(self):
        """Saving more than one location with the same name should fail."""
        data = {'description': 'fake location'}
        count = 0
        try:
            for i in range(100):
                content = JSONRenderer().render(data)
                stream = io.BytesIO(content)
                data = JSONParser().parse(stream)
                serializer = LocationSerializer(data=data)
                serializer.is_valid()
                serializer.save()
                count += 1
        except:
            pass
        
        # if count is 1, means only the first save worked
        self.assertEqual(count, 1)
        
        
class LocationUpdateSerializerTest(TestCase):
    def test_validate_post_data_1(self):
        """Validation should raise BadRequestException on no post data."""
        ser = LocationUpdateSerializer(data=None, many=True)
        with self.assertRaises(BadRequestException):
            ser.validate_post_data()
        
        
    def test_validate_post_data_2(self):
        """Validation should raise BadRequestException on wrong JSON format"""
        data = [{"id":1,"desc":"some place"}] # correct key is "description"
        ser = LocationUpdateSerializer(data=data, many=True)
        with self.assertRaises(BadRequestException):
            ser.validate_post_data()
        
    def test_validate_post_data_3(self):
        """Validation should raise BadRequestException when given jibberish data."""
        data = "jibberish"
        ser = LocationUpdateSerializer(data=data, many=True)
        with self.assertRaises(BadRequestException):
            ser.validate_post_data()
            
    def test_validate_post_data_4(self):
        """Validation should succeed with correct post data"""
        data = [{"id":1,"description":"some place"}]
        ser = LocationUpdateSerializer(data=data, many=True)
        ser.validate_post_data()
        
    def test_is_valid_1(self):
        """Validation method should return True when entries are found in the 
        database for corresponding post data."""
        # create entries
        locations = Location.objects.bulk_create(
                    [Location(id=1, description="loc 1"),
                     Location(id=2, description="loc 2"),
                     Location(id=3, description="loc 3")])
        # create data
        data = [{"id":1, "description":"some place 1"},
                {"id":2, "description":"some place 2"},
                {"id":3, "description":"some place 3"}]
        # create serializer
        ser = LocationUpdateSerializer(data=data, many=True)
        # set locations on serializer equal to entries
        ser.locations = locations
        # call method under test and assert return value is True
        ret = ser.is_valid()
        self.assertTrue(ret)
        
    def test_is_valid_2(self):
        """Validation method should return False when entries are NOT found in 
        the database for corresponding post data."""
        # create entries
        locations = Location.objects.bulk_create(
                    [Location(id=1, description="loc 1"),
                     Location(id=2, description="loc 2"),
                     Location(id=3, description="loc 3")])
        # create data
        data = [{"id":1, "description":"some place 1"},
                {"id":2, "description":"some place 2"},
                {"id":4, "description":"some place 3"}]
        # create serializer
        ser = LocationUpdateSerializer(data=data, many=True)
        # set locations on serializer equal to entries
        ser.locations = locations
        # call method under test and assert return value is False
        ret = ser.is_valid()
        self.assertFalse(ret)
        
        
    def test_save_1(self):
        """RuntimeError should be raised when no locations are set on the serializer."""
        data = [{"id":1, "description":"some place 1"}]
        ser = LocationUpdateSerializer(data=data, many=True)
        self.assertEqual(ser.locations, None)
        with self.assertRaises(RuntimeError):
            ser.save()
        
        
    def test_save_2(self):
        """Valid data and locations should bulk save correctly."""
        locations = Location.objects.bulk_create(
                    [Location(id=1, description="some place 1"),
                     Location(id=2, description="some place 2"),
                     Location(id=3, description="some place 3")])
            
        data = [{"id":1, "description":"updated place 1"},
                {"id":2, "description":"updated place 2"},
                {"id":3, "description":"updated place 3"}]
        
        ser = LocationUpdateSerializer(data=data, many=True)
        ser.locations = locations
        
        ser.save()
        
        # We started with three, so those three should have been updated and
        # no new locations created
        self.assertEqual(Location.objects.count(), 3)
        # Verify descriptions were updated
        locs = Location.objects.all()
        x = 1
        descriptions = ["updated place 1", "updated place 2", "updated place 3"]
        for loc in locs:
            self.assertEqual(loc.id, x)
            self.assertEqual(loc.description, descriptions[x-1])
            x += 1
            
        # No new locations should have been created.
        self.assertEqual(x, 4)
    
        
        
        
        
        