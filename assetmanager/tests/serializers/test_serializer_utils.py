# -*- coding: utf-8 -*-
from django.test import TestCase
from ...custom_api_exceptions import BadRequestException
from ...models import Asset, Location, Count
from ... import serializer_utils

# run with python manage.py test assetmanager.tests.serializers.test_serializers_utils
class SaveAssetLocationsTest(TestCase):
    
    def test_asset_locations_can_be_saved(self):
        """
        We should be able to save asset locations.
        """
        asset = Asset.objects.create(
                description="fake asset", original_cost=9999999999.99)
        loc1 = Location.objects.create(description='loc1')
        loc2 = Location.objects.create(description='loc2')
        
        locations = [
            {'location':'loc1','count':4},
            {'location':'loc2','count':50}
        ]
        
        serializer_utils.save_asset_locations(asset, locations)
        
        assert( len(Count.objects.all()) == 2 )
        
    
    def test_asset_locations_can_be_updated(self):
        """
        We should be able to save asset locations.
        """
        asset = Asset.objects.create(
                description="fake asset", original_cost=9999999999.99)
        loc1 = Location.objects.create(description='loc1')
        loc2 = Location.objects.create(description='loc2')
        Count.objects.create(asset=asset, location=loc1, count=25)
        Count.objects.create(asset=asset, location=loc2, count=30)
        
        locations = [
            {'location':'loc1','count':4},
            {'location':'loc2','count':50}
        ]
        
        serializer_utils.save_asset_locations(asset, locations)
        
        counts = Count.objects.all()
        assert( len(counts) == 2 )
        assert(counts[0].location == loc1 and counts[0].count == 4)
        assert(counts[1].location == loc2 and counts[1].count == 50)
    
    
    def test_asset_locations_can_be_deleted(self):
        """
        We should be able to delete asset locations via updation an asset's locations list.
        """
        asset = Asset.objects.create(
                description="fake asset", original_cost=9999999999.99)
        loc1 = Location.objects.create(description='loc1')
        loc2 = Location.objects.create(description='loc2')
        loc3 = Location.objects.create(description='loc3')
        Count.objects.create(asset=asset, location=loc1, count=100)
        Count.objects.create(asset=asset, location=loc2, count=100)
        Count.objects.create(asset=asset, location=loc3, count=100)
        
        loc4 = Location.objects.create(description='loc4')
        loc5 = Location.objects.create(description='loc5')
        locations = [
            {'location':'loc4','count':4},
            {'location':'loc5','count':50}
        ]
        
        counts = Count.objects.filter(asset=asset)
        serializer_utils.save_asset_locations(asset, locations)
        # original 3 counts should have been deleted and 2 added
        counts = Count.objects.filter(asset=asset)
        assert( len(counts) == 2 )
        assert(counts[0].location.description == 'loc4' and counts[0].count == 4)
        assert(counts[1].location.description == 'loc5' and counts[1].count == 50)
    
        
    def test_error_in_locations_list(self):
        """
        Trying to save a nonexistent location should raise an error.
        """
        asset = Asset.objects.create(
                description="fake asset", original_cost=9999999999.99)
        loc1 = Location.objects.create(description='loc1')
        loc2 = Location.objects.create(description='loc2')
        Count.objects.create(asset=asset, location=loc1, count=25)
        Count.objects.create(asset=asset, location=loc2, count=30)
        
        locations = [
            {'location':'loc100','count':4}, # location doesn't exists
            {'location':'loc2','count':50}
        ]
    
        exception_raised = False
        try:
            serializer_utils.save_asset_locations(asset, locations)
        except:
            exception_raised = True
        assert(exception_raised)