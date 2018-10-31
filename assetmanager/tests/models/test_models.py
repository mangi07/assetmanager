from django.test import TestCase

from ...models import Asset, Location, Count

# Create your tests here.
class AssetModelTests(TestCase):

    def test_asset_created_with_description(self):
        """
        An asset should be created with the given description.
        """
        thing1 = Asset(description="thing1", original_cost=100)
        thing1.save()
        assets = Asset.objects.all()
        self.assertEqual(thing1.description, "thing1")
        self.assertEqual(assets[0].description, "thing1")
        
class LocationModelTests(TestCase):
    
    def test_location_created_with_description(self):
        """
        A location should be created with the given description.
        """
        location1 = Location(description="location1")
        location1.save()
        locations = Location.objects.all()
        self.assertEqual(location1.description, "location1")
        self.assertEqual(locations[0].description, "location1")
        
class CountModelTests(TestCase):
    
    def test_asset_count_created_successfully(self):
        """
        Count should represent how many of one asset are at given location.
        """
        thing1 = Asset(description="thing1", original_cost=100)
        thing1.save()
        thing1 = None
        thing1 = Asset.objects.first()
        
        location1 = Location(description="location1")
        location1.save()
        location1 = None
        location1 = Location.objects.first()
        
        count = Count(asset=thing1, location=location1, count=5)
        count.save()
        count = None
        count = Count.objects.first()
        self.assertEqual(count.count, 5)
        self.assertEqual(count.asset, thing1)
        self.assertEqual(count.location, location1)
        