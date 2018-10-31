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


class GetAssetListTest(TestCase): 
    def setUp(self):
        self.thing1 = Asset.objects.create(
            description='thing one', original_cost=100)
        self.thing2 = Asset.objects.create(
            description='thing two', original_cost=200)
        self.client = Client()
        

    def test_asset_detail_returns_OK(self):
        response = self.client.get(
            reverse('asset-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(
            reverse('asset-detail', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_asset_detail_PUT_succeeds(self):
        # before PUT
        db_desc = Asset.objects.get(pk=2).description
        self.assertEqual(db_desc, 'thing two')
        
        description = 'thing one description has been changed'
        payload = {'description':description, 'original_cost':100}
        response = self.client.put(
                reverse('asset-detail', kwargs={'pk': 2}),
                json.dumps(payload),
                content_type="application/json"
        )
        
        # after PUT
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        ret_desc = json.loads(response.content)['description']
        self.assertEqual(ret_desc, description)
        
        db_desc = Asset.objects.get(pk=2).description
        self.assertEqual(db_desc, description)
        
        
    def test_asset_detail_PUT_fails_without_all_fields(self):
        old_desc = Asset.objects.get(pk=2).description
        change_desc = 'thing one description has been changed'
        payload = {'description':change_desc}
        response = self.client.put(
                reverse('asset-detail', kwargs={'pk': 2}),
                json.dumps(payload),
                content_type="application/json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        updated_desc = Asset.objects.get(pk=2).description
        self.assertEqual(updated_desc, old_desc)
        
    # TODO: test PATCH, DELETE
    # TODO: refactor into separate methods the creation of payloads and db entries used in all tests??
    # TODO: refactor tests to incorporate authentication and authorization
    # TODO: add JWT capability to API