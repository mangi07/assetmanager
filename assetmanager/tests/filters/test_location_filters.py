# -*- coding: utf-8 -*-
from django.test import TestCase
from ...custom_api_exceptions import BadRequestException
from ...models import Location
from ...filters import LocationFilter


class LocationFilterTest(TestCase):
    
    def test_all_filters(self):
        """filtering with all valid filters should work"""
        query_params = {"id":"12", "description":"something"}
        locations = Location.objects.all()
        locations_filter = LocationFilter(locations, query_params)
        filtered_queryset = locations_filter.qs()
        if not filtered_queryset:
            no_results = True
        self.assertEqual(no_results, True)
        
    def test_one_filter(self):
        """filtering with one valid filter should work"""
        Location.objects.create(description="something is here")
        Location.objects.create(description="something  else is here")
        
        query_params = {"description":"something is here"}
        locations = Location.objects.all()
        locations_filter = LocationFilter(locations, query_params)
        filtered_queryset = locations_filter.qs()
        self.assertEqual(len(filtered_queryset), 1)
        
    def test_typo_in_querystring(self):
        """filtering with misspelled querystring key should raise exception"""
        query_params = {"descriptions":"something"}
        locations = Location.objects.all()
        locations_filter = LocationFilter(locations, query_params)
        
        with self.assertRaises(BadRequestException):
            locations_filter.qs()
            
    # test good querystring but not found in db should return empty string
    def test_filter_returns_empty_results(self):
        """filter should accept query params but return empty result"""
        query_params = {"description":"something 2"}
        Location.objects.create(description="something1")
        Location.objects.create(description="something2")
        
        locations = Location.objects.all()
        locations_filter = LocationFilter(locations, query_params)
        filtered_queryset = locations_filter.qs()
        if not filtered_queryset:
            no_results = True
        self.assertEqual(no_results, True)
        
    # test good querystring where items present in db for one param but not the other
    def test_filter_returns_one_of_many_locations(self):
        """filter should filter one location out of many"""
        query_params = {"description":"something2"}
        Location.objects.create(description="something1")
        Location.objects.create(description="something2")
        Location.objects.create(description="something3")
        
        locations = Location.objects.all()
        locations_filter = LocationFilter(locations, query_params)
        filtered_queryset = locations_filter.qs()
        
        self.assertEqual(len(filtered_queryset), 1)
        self.assertEqual(filtered_queryset[0].description, "something2")
        
    def test_filter_like(self):
        """filter should filter several locations"""
        descs = ["Building1-rm201", "Building2-rm201", "Building3-rm101",
                 "House1-master", "House1-bathroom", "House1-kitchen",
                 "House2-master", "House2-bathroom", "House2-kitchen"]
        for desc in descs:
            Location.objects.create(description=desc)

        query_params = {"description__like":"House"}
        locations = Location.objects.all()
        locations_filter = LocationFilter(locations, query_params)
        filtered_queryset = locations_filter.qs()
        self.assertEqual(len(filtered_queryset), 6)
        for loc in filtered_queryset:
            self.assertIn("House", loc.description)
            
        query_params = {"description__like":"201"}
        locations_filter = LocationFilter(locations, query_params)
        filtered_queryset = locations_filter.qs()
        self.assertEqual(len(filtered_queryset), 2)
        for loc in filtered_queryset:
            self.assertIn("201", loc.description)
        
        
        
        