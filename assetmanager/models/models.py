from django.db import models

# Create your models here.
class Asset(models.Model):
    description = models.CharField(max_length=200)
    original_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.description


class Location(models.Model):
    description = models.CharField(max_length=200)
    assets = models.ManyToManyField(Asset, through='Count')
    
    def __str__(self):
        return self.description
    
    
class Count(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    count = models.IntegerField()
    
    def __int__(self):
        return self.count
    
