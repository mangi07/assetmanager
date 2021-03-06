# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

from ...models import Asset, Location, Count
from ...serializers import AssetSerializer, LocationSerializer, LocationUpdateSerializer
from ...custom_api_exceptions import BadRequestException

from jsonschema import validate
from ..schemas.utils import load_json_schema

from django.contrib.auth.models import User


class AssetSerializerTest(TestCase):
    
    def test_asset_can_be_serialized(self):
        """
        We should be able to serialize an asset:
            Create the expected dict representation.
        """
        asset = Asset.objects.create(
                description="fake asset", original_cost=9999999999.99)
        loc1 = Location.objects.create(description='loc1')
        loc2 = Location.objects.create(description='loc2')
        Count.objects.create(asset=asset, location=loc1, count=25)
        Count.objects.create(asset=asset, location=loc2, count=30)
        
        serializer = AssetSerializer(asset)
        json_schema = load_json_schema("asset_serializer.json")
        validate(serializer.data, json_schema)
        
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
        location = Location.objects.create(description="fake location")
        serializer = LocationSerializer(location)
        #self.assertDictEqual(serializer.data,
        #                     {'id': 1, 'description': 'fake location'})
        
        json_schema = load_json_schema("location_serializer.json")
        validate(serializer.data, json_schema)
    
    
    def test_location_can_be_deserialized(self):
        """Deserialize a location that has been correctly serialized:"""
        data = {'id': 1, 'description': 'fake location1'}
        
        """3. convert from json string back to raw python data structure"""
        content = JSONRenderer().render(data)
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = LocationSerializer(data=data)
        serializer.is_valid()
        assert(serializer.is_valid())
        
        """4. convert this data structure to Location object instance"""
        location = serializer.save()
        
        self.assertEqual(location.description, 'fake location1')
        
        
    def test_location_descriptions_must_be_unique_under_same_parent_location(self):
        """Should not create two locations with the same description when both share the same parent location."""
        # create parent location
        data = {'description': 'parent'}
        content = JSONRenderer().render(data)
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = LocationSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        assert(Location.objects.filter(pk=1).first().description == 'parent')
        
        # create child location
        data = {'description': 'child', 'in_location': 1}
        content = JSONRenderer().render(data)
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = LocationSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        
        # try to create another child location with same description
        data = {'description': 'child', 'in_location': 1}
        content = JSONRenderer().render(data)
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = LocationSerializer(data=data)
        with self.assertRaises(AssertionError):
            serializer.is_valid()
            serializer.save()
        
        
    def test_location_descriptions_with_no_parent_locations_must_be_unique(self):
        """Should not create two locations with the same description when both have no parent location."""
        # TODO
        pass
    
class LocationUpdateSerializerTest(TestCase):
    def test_validate_post_data_1(self):
        """Validation should raise BadRequestException on no post data."""
        user = User.objects.create(username='fake user')
        
        ser = LocationUpdateSerializer(user, data=None, many=True)
        with self.assertRaises(BadRequestException):
            ser.validate_post_data()
        
        
    def test_validate_post_data_2(self):
        """Validation should raise BadRequestException on wrong JSON format"""
        user = User.objects.create(username='fake user')
        
        data = [{"id":1,"desc":"some place"}] # correct key is "description"
        ser = LocationUpdateSerializer(user, data=data, many=True)
        with self.assertRaises(BadRequestException):
            ser.validate_post_data()
    
    
    def test_validate_post_data_3(self):
        """Validation should raise BadRequestException when given jibberish data."""
        user = User.objects.create(username='fake user')
        
        data = "jibberish"
        ser = LocationUpdateSerializer(user, data=data, many=True)
        with self.assertRaises(BadRequestException):
            ser.validate_post_data()
    
    
    def test_validate_post_data_4(self):
        """Validation should succeed with correct post data"""
        user = User.objects.create(username='fake user')
        
        data = [{"id":1,"description":"some place"}]
        ser = LocationUpdateSerializer(user, data=data, many=True)
        ser.validate_post_data()
    
    
    def test_is_valid_1(self):
        """Validation method should return True when entries are found in the
        database for corresponding post data."""
        user = User.objects.create(username='fake user')
        
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
        ser = LocationUpdateSerializer(user, data=data, many=True)
        # set locations on serializer equal to entries
        ser.locations = locations
        # call method under test and assert return value is True
        ret = ser.is_valid()
        self.assertTrue(ret)
    
    
    def test_is_valid_2(self):
        """Validation method should return False when entries are NOT found in
        the database for corresponding post data."""
        user = User.objects.create(username='fake user')
        
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
        ser = LocationUpdateSerializer(user, data=data, many=True)
        # set locations on serializer equal to entries
        ser.locations = locations
        # call method under test and assert return value is False
        ret = ser.is_valid()
        self.assertFalse(ret)
    
    
    def test_is_valid_3(self):
        """is_valid should return false because the location was not found."""
        user = User.objects.create(username='fake user')
        
        locations = Location.objects.bulk_create(
                    [Location(id=1, description="some place 1")])
        data = [{"id":100, "description":"updated place 1"}]
        ser = LocationUpdateSerializer(user, data=data, many=True)
        self.assertFalse(ser.is_valid())
        
        
    def test_is_valid_4(self):
        """is_valid should return false because some of the locations were not found."""
        user = User.objects.create(username='fake user')
        
        locations = Location.objects.bulk_create(
                    [Location(id=1, description="some place 1"),
                     Location(id=2, description="some place 2"),
                     Location(id=3, description="some place 3")]
                    )
        data = [{"id":100, "description":"updated place 100"},
                {"id":500, "description":"updated place 500"},
                {"id":1, "description":"updated place 1"},
                {"id":3, "description":"updated place 3"},
                {"id":21, "description":"updated place 1"}]
        ser = LocationUpdateSerializer(user, data=data, many=True)
        self.assertFalse(ser.is_valid())
        
        
    def test_save_1(self):
        """RuntimeError should be raised when no locations are set on the serializer."""
        user = User.objects.create(username='fake user')
        
        data = [{"id":1, "description":"some place 1"}]
        ser = LocationUpdateSerializer(user, data=data, many=True)
        self.assertEqual(ser.items, None)
        with self.assertRaises(RuntimeError):
            ser.save()
        
        
    def test_save_2(self):
        """Valid data and locations should bulk save correctly."""
        user = User.objects.create_superuser(username='fake user',
                                         email='fake@fake.com',
                                         password='password')
        
        locations = Location.objects.bulk_create(
                    [Location(id=1, description="some place 1"),
                     Location(id=2, description="some place 2"),
                     Location(id=3, description="some place 3")])
            
        data = [{"id":1, "description":"updated place 1"},
                {"id":2, "description":"updated place 2"},
                {"id":3, "description":"updated place 3"}]
        
        ser = LocationUpdateSerializer(user, data=data, many=True)
        ser.items = locations
        
        ser.save()
        
        # We started with three, so those three should have been updated and
        # no new locations created
        self.assertEqual(Location.objects.count(), 3)
        # Verify descriptions were updated
        locs = Location.objects.all()
        # TODO: may be more pythonic to order 2 lists and then compare them to assert equality
        x = 1
        descriptions = ["updated place 1", "updated place 2", "updated place 3"]
        for loc in locs:
            self.assertEqual(loc.id, x)
            self.assertEqual(loc.description, descriptions[x-1])
            x += 1
            
        # No new locations should have been created.
        self.assertEqual(x, 4)
        

    
    
        
        
        
        