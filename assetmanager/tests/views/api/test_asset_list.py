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
                            {"location":self.loc1.description, "count":100},
                            {"location":self.loc2.description, "count":0}
                    ]}
                for c in range(count)]
        return payload
    
    def make_assets(self):
        asset1 = Asset.objects.create(
            description='thing one', original_cost=100)
        asset2 = Asset.objects.create(
            description='thing two', original_cost=200)
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        Count.objects.create(asset=asset1, location=self.loc2, count=30)
        Count.objects.create(asset=asset2, location=self.loc2, count=30)
        
        
    def test_asset_list(self):
        self.make_assets()
        
        response = self.client.get(
            reverse('asset-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # TODO: Test asset listing with pagination and filtering once it's added.
        
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
        
    def test_patch_asset_list1(self):
        """Asset description should change with patch request"""
        self.make_assets()
        assets = Asset.objects.all().order_by('id')
        assert assets[0].description == "thing one"
        
        payload = [{"id":1, "description":"thing one changed"}]
        response = self.client.patch(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        assets = Asset.objects.all().order_by('id')
        self.assertEqual(assets[0].description, "thing one changed")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        json_schema = load_json_schema("asset_list_patch_response.json")
        validate(response.data, json_schema)
        
    def test_patch_asset_list2(self):
        """Asset description and cost should change with patch request"""
        self.make_assets()
        assets = Asset.objects.all().order_by('id')
        assert assets[0].description == "thing one"
        assert assets[0].original_cost == 100
        
        payload = [{"id":1, "description":"thing one changed", 
                    "original_cost":"99.95"}]
        response = self.client.patch(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        assets = Asset.objects.all().order_by('id')
        self.assertEqual(assets[0].description, "thing one changed")
        self.assertEqual(assets[0].original_cost, Decimal('99.95'))
        
        json_schema = load_json_schema("asset_list_patch_response.json")
        validate(response.data, json_schema)
    
    def test_patch_asset_list3(self):
        """Asset location count should change with patch request"""
        # start with asset 2 location 2 count 30 and test that it can be changed
        
        asset1 = Asset.objects.create(
            description='thing one', original_cost=100)
        asset2 = Asset.objects.create(
            description='thing two', original_cost=200)
        
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        Count.objects.create(asset=asset1, location=self.loc2, count=30)
        Count.objects.create(asset=asset2, location=self.loc2, count=30)
        
        counts = Count.objects.filter(asset=2,location=2) # asset id  and location        
        assert counts[0].count == 30
        
        payload = [{"id":2, "locations":[{"location":"loc2","count":31}]}]
        response = self.client.patch(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        counts = Count.objects.filter(asset=2,location=2)
        self.assertEqual(counts[0].count, 31)
        
        json_schema = load_json_schema("asset_list_patch_response.json")
        validate(response.data, json_schema)
        
    def test_patch_asset_list4(self):
        """Multiple fields should change with patch request"""
        
        asset1 = Asset.objects.create(
            description='thing one', original_cost=100)
        asset2 = Asset.objects.create(
            description='thing two', original_cost=200)
        
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        Count.objects.create(asset=asset1, location=self.loc2, count=30)
        Count.objects.create(asset=asset2, location=self.loc2, count=30)
        
        counts = Count.objects.filter(asset=1,location=1) # asset id  and location        
        assert counts[0].count == 25
        counts = Count.objects.filter(asset=2,location=2) # asset id  and location        
        assert counts[0].count == 30
        
        payload = [
                {"id":1, "locations":[{"location":"loc1","count":1}]},
                {"id":2, "locations":[{"location":"loc2","count":300}], "original_cost":"500.01"}
                ]
        response = self.client.patch(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        counts = Count.objects.filter(asset=1,location=1)
        self.assertEqual(counts[0].count, 1)
        counts = Count.objects.filter(asset=2,location=2)
        self.assertEqual(counts[0].count, 300)
        asset = Asset.objects.get(pk=2)
        self.assertEqual(asset.original_cost, Decimal('500.01'))
        
        json_schema = load_json_schema("asset_list_patch_response.json")
        validate(response.data, json_schema)
        
    def test_patch_asset_list5(self):
        """Should add new count (not new location) with patch request"""
        
        asset1 = Asset.objects.create(
            description='thing one', original_cost=100)
        asset2 = Asset.objects.create(
            description='thing two', original_cost=200)
        
        Count.objects.create(asset=asset1, location=self.loc1, count=25)
        
        # This should add location 2 to both assets
        payload = [
                {"id":1, "locations":[{"location":"loc2","count":1}]},
                {"id":2, "locations":[{"location":"loc2","count":300}]}
                ]
        response = self.client.patch(
                reverse('asset-list'),
                json.dumps(payload),
                content_type="application/json"
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        print(response.data)
        # TODO: find out why 'thing two' location count is 1
        
        json_schema = load_json_schema("asset_list_patch_response.json")
        validate(response.data, json_schema)
        
    # TODO: add JWT capability to API