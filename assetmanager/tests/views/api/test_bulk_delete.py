# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Asset, Location, Count
from ...schemas.utils import load_json_schema
from jsonschema import validate
from decimal import Decimal
import time


class BulkDeleteTest(TestCase):
    """Test APIView for listing and creating assets in bulk"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                         email='fake@fake.com',
                                         password='password')
        self.client.force_login(user=self.user)
        
        self.loc1 = Location.objects.create(description='loc1')
        self.loc2 = Location.objects.create(description='loc2')

    
    ############################################################
    # test bulk delete of assets
    def test_bulk_delete_assets1(self):
        """No data should return status 400"""
        #print("test bulk delete 1")
        response = self.client.post(
                reverse('asset-list-delete'),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bulk_delete_assets2(self):
        """Property in request json not a list returns status 400"""
        #print("test bulk delete 2")
        payload = {"key":"not a list here"}
        response = self.client.post(
                reverse('asset-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bulk_delete_assets3(self):
        """List property in request json not all numbers returns status 400"""
        #print("test bulk delete 3")
        payload = [1, "two is str", 3]
        response = self.client.post(
                reverse('asset-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bulk_delete_assets4(self):
        """test only some ids to delete exist, so none get deleted"""
        #print("test bulk delete 4")
        asset1 = Asset.objects.create(
            description='thing one', original_cost=100)
        asset2 = Asset.objects.create(
            description='thing two', original_cost=200)
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        Count.objects.create(asset=asset1, location=self.loc2, count=30)
        Count.objects.create(asset=asset2, location=self.loc2, count=30)
                
        locations = Location.objects.all()
        assert len(locations) == 2
        counts = Count.objects.all()
        assert len(counts) == 3
        
        payload = [1,2,3]
        response = self.client.post(
                reverse('asset-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        locations = Location.objects.all()
        self.assertEqual(len(locations), 2)
        assets = Asset.objects.all()
        self.assertEqual(len(assets), 2)
        
    def test_bulk_delete_assets5(self):
        """test successfully delete one asset"""
        #print("test bulk delete 5")
        Asset.objects.create(description="thing 1", original_cost=500)
        Asset.objects.create(description="thing 2", original_cost=1500)
        assert Asset.objects.count() == 2
        
        payload = [1]
        response = self.client.post(
                reverse('asset-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Asset.objects.count(), 1)
    
    def test_bulk_delete_assets6(self):
        """test successfully delete multiple assets"""
        #print("test bulk delete 6")
        Asset.objects.create(description="thing 1", original_cost=500)
        Asset.objects.create(description="thing 2", original_cost=1500)
        assert Asset.objects.count() == 2
        
        payload = [1,2]
        response = self.client.post(
                reverse('asset-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Asset.objects.count(), 0)
    
    def test_bulk_delete_assets7(self):
        """test deletion of assets with location counts delete the correct counts but not the involved locations"""
        #print("test bulk delete 7")
        asset1 = Asset.objects.create(description="thing 1", original_cost=500)
        asset2 = Asset.objects.create(description="thing 2", original_cost=1500)
        assert Asset.objects.count() == 2
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        Count.objects.create(asset=asset1, location=self.loc2, count=30)
        Count.objects.create(asset=asset2, location=self.loc2, count=35)
        assert Count.objects.count() == 3
        # now 'thing 1' has 2 counts and 'thing 2' has 1 count, and there are 2 locations
        
        payload = [2]
        response = self.client.post(
                reverse('asset-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        # 'thing 2' and it's count of 30 at loc2 should have been deleted
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Asset.objects.count(), 1) # one less asset
        self.assertEqual(Count.objects.count(), 2) # one less count
        self.assertEqual(Location.objects.count(), 2) # no locations deleted
        
        asset1 = Asset.objects.get(pk=1)
        counts = Count.objects.filter(asset=1)
        self.assertEqual(asset1.description, "thing 1") # correct asset remains
        # the assets location counts remain unchanged
        self.assertEqual(counts[0].count, 25)
        self.assertEqual(counts[1].count, 30)
    
    
    ############################################################
    # test bulk delete of locations
    def test_bulk_delete_locations1(self):
        """No data should return status 400"""
        #print("test bulk delete locations 1")
        response = self.client.post(
                reverse('location-list-delete'),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bulk_delete_locations2(self):
        """Property in request json not a list returns status 400"""
        #print("test bulk delete locations 2")
        payload = {"key":"not a list here"}
        response = self.client.post(
                reverse('location-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bulk_delete_locations3(self):
        """List property in request json not all numbers returns status 400"""
        #print("test bulk delete locations 3")
        #loc1 = Location.objects.create(
        #    description='thing one')
        #loc2 = Location.objects.create(
        #    description='thing two')
        assert Location.objects.count() == 2
        
        payload = [1, "two is str", 3]
        response = self.client.post(
                reverse('location-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 2)
        
    def test_bulk_delete_locations4(self):
        """test only some ids to delete exist, so none get deleted"""
        #print("test bulk delete locations 4")
        #loc1 = Location.objects.create(
        #    description='thing one')
        #loc2 = Location.objects.create(
        #    description='thing two')
                
        locations = Location.objects.all()
        assert len(locations) == 2
        
        payload = [1,2,3]
        response = self.client.post(
                reverse('location-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        locations = Location.objects.all()
        self.assertEqual(len(locations), 2)
        
    def test_bulk_delete_locations5(self):
        """test successfully delete one location"""
        #print("test bulk delete locations 5")
        #loc1 = Location.objects.create(
        #    description='thing one')
        #loc2 = Location.objects.create(
        #    description='thing two')
        locations = Location.objects.all()
        assert len(locations) == 2
         
        payload = [1]
        response = self.client.post(
                reverse('location-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Location.objects.count(), 1)
    
    def test_bulk_delete_locations6(self):
        """test successfully delete multiple locations"""
        #print("test bulk delete locations 6")
        #loc1 = Location.objects.create(
        #    description='thing one')
        #loc2 = Location.objects.create(
        #    description='thing two')
        locations = Location.objects.all()
        assert len(locations) == 2
         
        payload = [1, 2]
        response = self.client.post(
                reverse('location-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Location.objects.count(), 0)
    
    def test_bulk_delete_locations7(self):
        """test cannot delete locations that are part of an asset count"""
        #print("test bulk delete locations 7")
        #loc1 = Location.objects.create(
        #    description='thing one')
        #loc2 = Location.objects.create(
        #    description='thing two')
        locations = Location.objects.all()
        assert len(locations) == 2
        asset1 = Asset.objects.create(description="thing 1", original_cost=500)
        asset2 = Asset.objects.create(description="thing 2", original_cost=1500)
        assert Asset.objects.count() == 2
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        Count.objects.create(asset=asset1, location=self.loc2, count=30)
        Count.objects.create(asset=asset2, location=self.loc2, count=35)
        assert Count.objects.count() == 3
        
         
        payload = [1, 2]
        response = self.client.post(
                reverse('location-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 2)
    
    def test_bulk_delete_locations8(self):
        """test neither location is deleted when only one is part of an asset count"""
        #print("test bulk delete locations 8")
        #loc1 = Location.objects.create(
        #    description='thing one')
        #loc2 = Location.objects.create(
        #    description='thing two')
        locations = Location.objects.all()
        assert len(locations) == 2
        asset1 = Asset.objects.create(description="thing 1", original_cost=500)
        asset2 = Asset.objects.create(description="thing 2", original_cost=1500)
        assert Asset.objects.count() == 2
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        assert Count.objects.count() == 1
        
        payload = [1, 2]
        response = self.client.post(
                reverse('location-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 2)
        
    def test_bulk_delete_locations9(self):
        """test neither location is deleted when request format is invalid"""
        #print("test bulk delete locations 9")
        #loc1 = Location.objects.create(
        #    description='thing one')
        #loc2 = Location.objects.create(
        #    description='thing two')
        locations = Location.objects.all()
        assert len(locations) == 2
        
        payload = {'key':'blah, blah'}
        response = self.client.post(
                reverse('location-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 2)
    
    # TODO: remove old way of bulk deleting through the other route

