# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Location


class LocationListTest(TestCase):
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
        payload = [{"description":"abc"+str(c)} for c in range(count)]
        return payload
        
    def test_GET_location_list(self):
        response = self.client.get(
            reverse('location-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_json = """[
            {
                "id": 1,
                "description": "loc1"
            },
            {
                "id": 2,
                "description": "loc2"
             }
        ]"""
        actual_json = response.content.decode('utf8').replace("'", '"')
        self.assertEqual(json.loads(actual_json), json.loads(expected_json))
        
    # TODO: Test location listing with pagination and filtering once it's added.

    def test_add_one_location(self):
        payload = self.make_payload(1)
        response = self.client.post(
                reverse('location-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(json.loads(response.content)), 1)


    def test_add_more_than_one_asset(self):
        payload = self.make_payload(2)
        response = self.client.post(
                reverse('location-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(json.loads(response.content)), 2)

"""
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
        
    def test_cannot_add_asset_with_duplicate_locations(self):
        prev_asset_count = Asset.objects.count()
        payload = self.make_payload(1)
        payload[0]['locations'] = [
                            {"location":self.loc2.description, "count":100},
                            {"location":self.loc2.description, "count":0}
                    ]
        response = self.client.post(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        new_asset_count = Asset.objects.count()
        self.assertEqual(new_asset_count, prev_asset_count)
"""
       
    # TODO: add JWT capability to API# -*- coding: utf-8 -*-

