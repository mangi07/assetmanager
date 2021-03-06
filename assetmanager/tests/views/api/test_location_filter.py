import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Location


class LocationFilterTestAPI(TestCase):
    """Test APIView for filtering location list returned by GET"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',
                                         email='fake@fake.com',
                                         password='password')
        self.client.force_login(user=self.user)

    
    def test_location_filter_returns_empty(self):
        """should return empty list"""
        response = self.client.get(
            reverse('location-list'), {'description':'nonexistent'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)['results']
        self.assertEqual([], results)
        
    def test_location_filter_returns_one(self):
        """should return the only match for the filter"""
        Location.objects.create(description="one")
        Location.objects.create(description="two")
        Location.objects.create(description="three")
        
        response = self.client.get(
            reverse('location-list'), {'description':'two'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 1)
        
        id = results[0]['id']
        descr = results[0]['description']
        self.assertEqual(id, 2)
        self.assertEqual(descr, "two")
        
    def test_location_filter_returns_multiple_matches(self):
        """should return more than one match for the filter"""
        Location.objects.create(description="one fish")
        Location.objects.create(description="two fish")
        Location.objects.create(description="red fish")
        Location.objects.create(description="another red fish")
        
        response = self.client.get(
            reverse('location-list'), {'description__like':'fish'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 4)
        for loc in results:
            self.assertIn("fish", loc["description"])
        
        response = self.client.get(
            reverse('location-list'), {'description__like':'red'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 2)
        for loc in results:
            self.assertIn("red", loc["description"])
            
    
    def test_location_filter_missing_query_values(self):
        """should return an empty list because no values were given in query string"""
        Location.objects.create(description="one fish")
        Location.objects.create(description="two fish")
        
        response = self.client.get(
            reverse('location-list'), {'description__like':None}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        results = obj['results']
        self.assertEqual(len(results), 0)