import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ....models import Location


class LocationFilterTestAPI(TestCase):
    """Test APIView for listing and creating assets in bulk"""

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
        self.assertEqual([], json.loads(response.content))
        
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
        self.assertEqual(len(obj), 1)
        self.assertListEqual([{"id":2,"description":"two"}], obj)
        
    def test_location_filter_returns_multiple_matches(self):
        """should return the only match for the filter"""
        Location.objects.create(description="one fish")
        Location.objects.create(description="two fish")
        Location.objects.create(description="red fish")
        Location.objects.create(description="another red fish")
        
        response = self.client.get(
            reverse('location-list'), {'description_like':'fish'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        self.assertEqual(len(obj), 4)
        for loc in obj:
            self.assertIn("fish", loc["description"])
        
        response = self.client.get(
            reverse('location-list'), {'description_like':'red'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        self.assertEqual(len(obj), 2)
        for loc in obj:
            self.assertIn("red", loc["description"])
            
    
    def test_location_filter_missing_query_values(self):
        """should return an empty list because no values were given in query string"""
        Location.objects.create(description="one fish")
        Location.objects.create(description="two fish")
        
        response = self.client.get(
            reverse('location-list'), {'description_like':None}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = json.loads(response.content)
        self.assertEqual(len(obj), 0)