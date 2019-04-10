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
    def test_bulk_delete1(self):
        """No data should return status 400"""
        response = self.client.post(
                reverse('asset-list-delete'),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bulk_delete2(self):
        """Property in request json not a list returns status 400"""
        payload = {"key":"not a list here"}
        response = self.client.post(
                reverse('asset-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bulk_delete3(self):
        """List property in request json not all numbers returns status 400"""
        payload = [1, "two is str", 3]
        response = self.client.post(
                reverse('asset-list-delete'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_bulk_delete4(self):
        """test only some ids to delete exist, so none get deleted"""
        asset1 = Asset.objects.create(
            description='thing one', original_cost=100)
        asset2 = Asset.objects.create(
            description='thing two', original_cost=200)
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        Count.objects.create(asset=asset1, location=self.loc2, count=30)
        Count.objects.create(asset=asset2, location=self.loc2, count=30)
                
        locations = Location.objects.all()
        assert len(locations) == 2
        
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
        
    def test_bulk_delete5(self):
        """test successfully delete one asset"""
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
    
    def test_bulk_delete6(self):
        """test successfully delete multiple assets"""
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
        
    # TODO: test deletion of assets with location counts
    # TODO: test deletion of locations once locations/bulkDelete functionality is added
    # TODO: remove old way of bulk deleting through the other route

