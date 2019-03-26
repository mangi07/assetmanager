from django.test import TestCase

from ...models import Location

# run with python manage.py test assetmanager.tests.models.test_location_model 
class AssetModelTests(TestCase):

    def test_locations_in_location(self):
        """
        A location should be able to belong to another location
        (each location owned by exactly one location 
        through foreign key or none).
        
        The idea is that a more general location can have 0 or more
        specific locations.
        """
        print("testing locations in location")
        building1 = Location(description = "building 1")
        building1.save()
        
        room1 = Location(description = "room 1", in_location = building1)
        room1.save()
        room2 = Location(description = "room 2", in_location = building1)
        room2.save()
        
        rooms_in_building = building1.locations.all()
        
        self.assertEqual(len(rooms_in_building), 2)
        

