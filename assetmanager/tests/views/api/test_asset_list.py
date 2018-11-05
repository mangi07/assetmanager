# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Asset, Location, Count


class AssetListTest(TestCase):
    """Test APIView for listing and creating assets"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                         email='fake@fake.com',
                                         password='password')
        self.client.force_login(user=self.user)
        
    def make_payload(self, count):
        payload = [{"description":"thing "+str(c+1), "original_cost":0} 
                for c in range(count)]
        return payload
        
    def test_asset_list(self):
        Asset.objects.create(
            description='thing one', original_cost=100)
        Asset.objects.create(
            description='thing two', original_cost=200)
        
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