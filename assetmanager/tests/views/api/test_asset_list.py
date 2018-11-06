# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Asset, Location, Count


class AssetListTest(TestCase):
    """Test APIView for listing and creating assets in bulk"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                         email='fake@fake.com',
                                         password='password')
        self.client.force_login(user=self.user)
        
        self.loc1 = Location.objects.create(description='loc1')
        self.loc2 = Location.objects.create(description='loc2')
        
    def make_payload(self, count):
        payload = [{"description":"thing "+str(c+1), "original_cost":0,
                    "locations":[
                            {"location":self.loc1.description, "count":count},
                            {"location":self.loc1.description, "count":count/2}
                    ]}
                for c in range(count)]
        return payload
        
    def test_asset_list(self):
        asset1 = Asset.objects.create(
            description='thing one', original_cost=100)
        asset2 = Asset.objects.create(
            description='thing two', original_cost=200)
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        Count.objects.create(asset=asset1, location=self.loc2, count=30)
        Count.objects.create(asset=asset2, location=self.loc2, count=30)
        
        response = self.client.get(
            reverse('asset-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # TODO: Test asset listing with pagination once it's added.
        
    def test_add_one_asset(self):
        payload = self.make_payload(1)
        response = self.client.post(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(json.loads(response.content)), 1)
        
    def test_add_more_than_one_asset(self):
        payload = self.make_payload(2)
        response = self.client.post(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_cannot_add_asset_with_payload_error(self):
        payload = ["blah blah"]
        response = self.client.post(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_cannot_add_asset_with_empty_payload(self):
        payload = None
        response = self.client.post(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # TODO: refactor into separate methods the creation of payloads and db entries used in all tests??
    # TODO: add JWT capability to API