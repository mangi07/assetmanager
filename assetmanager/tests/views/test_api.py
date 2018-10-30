# -*- coding: utf-8 -*-
import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from ...models import Asset


class AssetListTest(TestCase):
    """Test APIView for listing and creating assets"""
    def setUp(self):
        self.client = Client()
        
    def make_payload(self, count):
        payload = [{"description":"thing "+str(c+1)} for c in range(count)]
        return payload
        
    def test_asset_list(self):
        Asset.objects.create(
            description='thing one')
        Asset.objects.create(
            description='thing two')
        
        response = self.client.get(
            reverse('asset-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_add_one_asset(self):
        payload = self.make_payload(1)
        response = self.client.post(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_add_more_than_one_asset(self):
        payload = self.make_payload(2)
        response = self.client.post(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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


class GetAssetListTest(TestCase):
    
    
    def setUp(self):
        self.thing1 = Asset.objects.create(
            description='thing one')
        self.thing2 = Asset.objects.create(
            description='thing two')
        self.client = Client()

    

    def test_asset_detail(self):
        response = self.client.get(
            reverse('asset-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        json_string = """{"id":1, "description":"thing one"}"""
        data = json.loads(json_string)
        self.assertEqual(response.json(), data)
        
        response = self.client.get(
            reverse('asset-detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        json_string = """{"id":2, "description":"thing two"}"""
        data = json.loads(json_string)
        self.assertEqual(response.json(), data)