import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Asset, Location, Count


class LocationFilterTestAPI(TestCase):
    """Test APIView for filtering asset list returned by GET"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                         email='fake@fake.com',
                                         password='password')
        self.client.force_login(user=self.user)

    
    def test_asset_filter_returns_empty(self):
        """should return empty list"""
        response = self.client.get(
            reverse('asset-list'), {'description':'nonexistent'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)['results']
        self.assertEqual([], results)
        
    def test_asset_filter_returns_one(self):
        """should return the only match for the filter"""
        Asset.objects.create(description="one", original_cost="1")
        Asset.objects.create(description="two", original_cost="1")
        Asset.objects.create(description="three", original_cost="1")
        
        response = self.client.get(
            reverse('asset-list'), {'description':'two'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 1)
        
        id = results[0]['id']
        descr = results[0]['description']
        self.assertEqual(id, 2)
        self.assertEqual(descr, "two")
        
    def test_asset_filter_returns_multiple_matches(self):
        """should return more than one match for the filter"""
        Asset.objects.create(description="one fish", original_cost="1")
        Asset.objects.create(description="two fish", original_cost="1")
        Asset.objects.create(description="red fish", original_cost="1")
        Asset.objects.create(description="another red fish", original_cost="1")
        
        response = self.client.get(
            reverse('asset-list'), {'description__like':'fish'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 4)
        for loc in results:
            self.assertIn("fish", loc["description"])
        
        response = self.client.get(
            reverse('asset-list'), {'description__like':'red'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 2)
        for loc in results:
            self.assertIn("red", loc["description"])
            
    
    def test_asset_filter_missing_query_values(self):
        """should return an empty list because no values were given in query string"""
        Asset.objects.create(description="one fish", original_cost="1")
        Asset.objects.create(description="two fish", original_cost="1")
        
        response = self.client.get(
            reverse('asset-list'), {'description__like':None}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 0)

        
    def test_asset_filter_less_than(self):
        """should return one item less than original cost of 2000"""
        Asset.objects.create(description="one fish", original_cost="1999.99")
        Asset.objects.create(description="two fish", original_cost="2000.00")
        
        response = self.client.get(
            reverse('asset-list'), {'original_cost__lt':2000}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['description'], "one fish")
        
        
    def test_asset_filter_greater_than(self):
        """should return one item greater than original cost of 2000"""
        Asset.objects.create(description="one fish", original_cost="2000.01")
        Asset.objects.create(description="two fish", original_cost="2000.00")
        
        response = self.client.get(
            reverse('asset-list'), {'original_cost__gt':2000}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['description'], "one fish")
        
        
    def test_asset_filter_less_than_and_greater_than(self):
        """should return two items > 2000 and < 10000"""
        Asset.objects.create(description="one fish", original_cost="2000.00")
        Asset.objects.create(description="two fish", original_cost="2000.01")
        Asset.objects.create(description="red fish", original_cost="9999.99")
        Asset.objects.create(description="blue fish", original_cost="10000.00")
        
        response = self.client.get(
            reverse('asset-list'), {
                    'original_cost__gt':2000, 'original_cost__lt':10000}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['description'], "two fish")
        self.assertEqual(results[1]['description'], "red fish")
        
        
    def test_asset_filter_location(self):
        """should return assets matching given location"""
        asset1 = Asset.objects.create(description="one fish", original_cost="1")
        asset2 = Asset.objects.create(description="two fish", original_cost="1")
        asset3 = Asset.objects.create(description="red fish", original_cost="1")
        asset4 = Asset.objects.create(description="blue fish", original_cost="1")
        
        loc1 = Location.objects.create(description="loc1")
        loc2 = Location.objects.create(description="loc2")
        
        Count.objects.create(asset=asset1, location=loc1, count=1)
        Count.objects.create(asset=asset1, location=loc2, count=1)
        Count.objects.create(asset=asset2, location=loc2, count=1)
        Count.objects.create(asset=asset3, location=loc2, count=1)
        Count.objects.create(asset=asset4, location=loc1, count=1)
        
        response = self.client.get(
            reverse('asset-list'), {'location':'loc1'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['description'], "one fish")
        self.assertEqual(results[1]['description'], "blue fish")
        
        response = self.client.get(
            reverse('asset-list'), {'location':'loc2'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['description'], "one fish")
        self.assertEqual(results[1]['description'], "two fish")
        self.assertEqual(results[2]['description'], "red fish")
        

    def test_asset_filter_location_and_greater_than(self):
        """should return assets matching given location and greater than"""
        asset1 = Asset.objects.create(description="one fish", original_cost="50")
        asset2 = Asset.objects.create(description="two fish", original_cost="100")
        asset3 = Asset.objects.create(description="red fish", original_cost="200")
        asset4 = Asset.objects.create(description="blue fish", original_cost="400")
        
        loc1 = Location.objects.create(description="loc1")
        loc2 = Location.objects.create(description="loc2")
        
        Count.objects.create(asset=asset1, location=loc1, count=1)
        Count.objects.create(asset=asset2, location=loc1, count=1)
        Count.objects.create(asset=asset3, location=loc1, count=1)
        Count.objects.create(asset=asset4, location=loc2, count=1)
        
        response = self.client.get(
            reverse('asset-list'), {'location':'loc1', 'original_cost__gt':100}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['description'], "red fish") 