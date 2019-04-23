from django.db import models
from django.utils.timezone import now


#   should not create two locations with the same description when both share the same parent location
#   You should not be able to delete a location that is in a count.
class Location(models.Model):
    description = models.CharField(max_length=200)
    created = models.DateTimeField(default=now, db_index=True)
    in_location = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='locations')
    
    # prints this location's subnesting.
    # For example, if this location's description is 'room1' in location 'building1'
    # then this method will return 'building1 >> room1'
    @property
    def location_nesting(self):
        locs = [self.description]
        curr = self
        s = ""
        while curr is not None:
            curr = curr.in_location
            if curr is not None:
                locs.append(curr.description)
        while len(locs) > 1:
            s += locs.pop() + " >> "
        s += locs.pop()
        return s
    
    def __str__(self):
        return self.description
        
    class Meta:
        unique_together = ('description', 'in_location')


class Asset(models.Model):
    description = models.CharField(max_length=200)
    original_cost = models.DecimalField(max_digits=12, decimal_places=2)
    locations = models.ManyToManyField(Location, through='Count')
    created = models.DateTimeField(default=now, db_index=True)

    def __str__(self):
        return self.description

    
class Count(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)  # TODO: test that this prevents deleting a location in a count
    count = models.IntegerField()
    
    def __int__(self):
        return self.count
    
    class Meta:
        unique_together = ('asset', 'location',)
    
