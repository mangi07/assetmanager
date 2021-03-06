# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Location
from jsonschema import validate
from ...schemas.utils import load_json_schema


class LocationListTest(TestCase):
    """Test APIView for listing and creating assets in bulk"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser',
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
        actual_json_str = response.content.decode('utf8').replace("'", '"')
        actual_json = json.loads(actual_json_str)
        json_schema = load_json_schema("location_list.json")
        validate(actual_json, json_schema)
        
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


    def test_add_more_than_one_location(self):
        payload = self.make_payload(2)
        response = self.client.post(
                reverse('location-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(json.loads(response.content)), 2)
               
    def test_update_one_location(self):
        assert self.loc1.id == 1
        assert self.loc1.description == "loc1"
        payload = [{"id":"1","description":"loc1 changed"}]
        response = self.client.patch(
                reverse('location-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)
        loc1 = Location.objects.get(pk=1)
        self.assertEqual(loc1.description, "loc1 changed")

    def test_update_one_location2(self):
        """correct location updated where two locations exist with the same description
        but nested under different parent locations"""
        # setup 2 locations:
        # parent >> child
        # child
        parent = Location(description='parent')
        parent.save()
        child = Location(description='child', in_location=parent)
        child.save()
        child2 = Location(description='child')
        child2.save()
        
        # update child to 'child updated'
        payload = [{"id":str(child2.id),"description":"child updated"}]
        response = self.client.patch(
                reverse('location-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # parent >> child location should not have changed
        p = Location.objects.get(description="parent")
        loc = Location.objects.get(in_location=p)
        self.assertEqual(loc.description, "child")
        
        # child location (the one with no parent) should have changed to 'child updated'
        locs = Location.objects.filter(description='child updated')
        self.assertEqual(len(locs), 1)
        self.assertEqual(locs[0].in_location, None)

        
# TODO: add JWT capability to API

