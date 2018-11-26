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


    def test_DELETE_cannot_delete_non_existent_location_1(self):
        locs = Location.objects.all()
        loc_ids = [loc.id for loc in locs]
        
        # make a non-existent id
        id = sorted(loc_ids)[-1] + 1
        
        prev_count = Location.objects.count()
        
        response = self.client.delete(
                reverse('location-list'),
                json.dumps([id]),
                content_type="application/json"
            )
        
        new_count = Location.objects.count()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(prev_count, new_count)
        
        
    def test_DELETE_cannot_delete_non_existent_location_2(self):
        """no locations should be deleted when at least one id does not exist"""
        locs = Location.objects.all()
        loc_ids = [loc.id for loc in locs]
        
        # make a non-existent id
        id = sorted(loc_ids)[-1] + 1
        # replace an existing id with non-existing id
        loc_ids[-1] = id
        
        prev_count = Location.objects.count()
        
        response = self.client.delete(
                reverse('location-list'),
                json.dumps(loc_ids),
                content_type="application/json"
            )
        
        new_count = Location.objects.count()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(prev_count, new_count)
        
    
    def test_DELETE_one_location(self):
        """should be able to delete one location given its id"""
        locs = Location.objects.all()
        loc_ids = [loc.id for loc in locs]
        payload = [loc_ids[0]]
        
        prev_count = Location.objects.count()
        
        response = self.client.delete(
                reverse('location-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        new_count = Location.objects.count()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(prev_count, new_count+1)
        
    def test_DELETE_two_locations(self):
        """should be able to delete both locations given their ids"""
        locs = Location.objects.all()
        loc_ids = [loc.id for loc in locs]
        
        prev_count = Location.objects.count()
        
        response = self.client.delete(
                reverse('location-list'),
                json.dumps(loc_ids),
                content_type="application/json"
            )
        
        new_count = Location.objects.count()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(prev_count, 2)
        self.assertEqual(new_count, 0)
        
# TODO: add JWT capability to API

