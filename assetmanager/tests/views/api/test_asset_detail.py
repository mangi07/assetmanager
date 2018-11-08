# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Asset, Location, Count


class GetAssetListTest(TestCase): 
    def setUp(self):
        self.thing1 = Asset.objects.create(
            description='thing one', original_cost=100)
        self.thing2 = Asset.objects.create(
            description='thing two', original_cost=200)
        
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                         email='fake@fake.com',
                                         password='password')
        self.client.force_login(user=self.user)
        

    def test_asset_detail_GET_succeeds(self):
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

     
    def test_asset_detail_PATCH_succeeds(self):
        # before PATCH
        db_desc = Asset.objects.get(pk=2).description
        self.assertEqual(db_desc, 'thing two')
        
        description = 'thing one description has been changed'
        payload = {'description':description}
        response = self.client.patch(
                reverse('asset-detail', kwargs={'pk': 2}),
                json.dumps(payload),
                content_type="application/json"
        )
        
        # after PATCH
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        ret_desc = json.loads(response.content)['description']
        self.assertEqual(ret_desc, description)
        
        db_desc = Asset.objects.get(pk=2).description
        self.assertEqual(db_desc, description)
        
    def test_asset_detail_PATCH_existing_location_succeeds(self):
        # before PATCH
        asset = Asset.objects.get(pk=2)
        location = Location.objects.create(description='loc1')
        count = Count.objects.create(asset=asset, location=location, count=5)
        self.assertEqual(count.asset.description, 'thing two')
        
        payload = {'locations':[{'location':'loc1','count':10}]}
        response = self.client.patch(
                reverse('asset-detail', kwargs={'pk': 2}),
                json.dumps(payload),
                content_type="application/json"
        )
        
        # after PATCH
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Count.objects.first().count, 10)
        self.assertEqual(Count.objects.count(), 1)
        
    def test_asset_detail_PATCH_nonexisting_location_fails(self):
        # before PATCH
        asset = Asset.objects.get(pk=2)
        location = Location.objects.create(description='real location')
        count = Count.objects.create(asset=asset, location=location, count=5)
        self.assertEqual(count.asset.description, 'thing two')
        
        payload = {'locations':[{'location':'fake location','count':10}]}
        response = self.client.patch(
                reverse('asset-detail', kwargs={'pk': 2}),
                json.dumps(payload),
                content_type="application/json"
        )
        
        #print(response.content)
        # after PATCH
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Count.objects.first().count, 5)
        

    def test_asset_detail_DELETE_succeeds(self):
        asset = Asset.objects.get(pk=2)
        loc1 = Location.objects.create(description='loc1')
        loc2 = Location.objects.create(description='loc2')
        Count.objects.create(asset=asset, location=loc1, count=25)
        Count.objects.create(asset=asset, location=loc2, count=30)
        
        asset_count_before = Asset.objects.count()
        location_count_before = Location.objects.count()
        counts_before = Count.objects.count()
        
        self.client.delete(
                reverse('asset-detail', kwargs={'pk': 2}),
        )
        
        asset_count_after = Asset.objects.count()
        location_count_after = Location.objects.count()
        counts_after = Count.objects.count()
        
        # expect one less asset
        self.assertEqual(asset_count_before, asset_count_after+1)
        # expect both counts deleted
        self.assertEqual(counts_before, counts_after+2)
        # expect both locations still exist
        self.assertEqual(location_count_before, location_count_after)
        
    # TODO: add JWT capability to API# -*- coding: utf-8 -*-

