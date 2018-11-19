from django.db import models

# TODO: Create view and url for CRUD on locations
# TODO: Test CRUD, including the following: 
#   should not create two locations with the same description,
#   if location is deleted, all counts with that location will also be deleted
class Location(models.Model):
    description = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.description


class Asset(models.Model):
    description = models.CharField(max_length=200)
    original_cost = models.DecimalField(max_digits=12, decimal_places=2)
    locations = models.ManyToManyField(Location, through='Count')

    def __str__(self):
        return self.description

    
class Count(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    count = models.IntegerField()
    
    def __int__(self):
        return self.count
    
    class Meta:
        unique_together = ('asset', 'location',)
    
