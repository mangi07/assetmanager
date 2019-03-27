# -*- coding: utf-8 -*-
from .custom_api_exceptions import BadRequestException
from .models import Asset, Location, Count
from django.db import transaction

def find_duplicate_descs(descs):
    while(len(descs) > 0):
        desc = descs.pop()
        if desc in descs:
            return desc
    return None

@transaction.atomic
def save_asset_locations(asset, locations):
    """
    A list of counts per location is given for the asset.
    
    If the there is already a count of the asset at a given location,
    it will be updated.  Otherwise, the given location count will
    be newly associated with the asset. Any errors should result in
    no updates or saves (ie: uses atomic transaction).
    
    **PAY ATTENTION**
    A location count for an asset will be deleted if not in update_counts,
    the list of locations to be updated!!
    """
    
    # fail if duplicate locations are given
    descs = [loc['location'] for loc in locations]
    dup_descr = find_duplicate_descs(descs)
    if dup_descr:
        raise BadRequestException(
            ("Duplicate locations given: '{}'".format(dup_descr))
        )
    
    for location in locations:
        descr = location['location']
        count = location['count']
        # this filter returns None if location description not found
        loc = Location.objects.filter(description=descr).first()
        if not loc:
            raise BadRequestException(
                    ("'{}' location does not exist."
                     "  You need to first create the location before "
                     "trying to add an asset count to it.".format(descr))
                )
        
        # update count if it exists, otherwise create it
        location_count = Count.objects.filter(asset=asset, location=loc).first()
        if location_count:
            location_count.count = count
            location_count.save()
            #Count.objects.update(location=loc, count=count)
        else:
            Count.objects.create(asset=asset, location=loc, count=count)
    
    # remove location associations not in the list
    descs = [loc['location'] for loc in locations]
    location_objs = Location.objects.filter(description__in=descs)
    update_counts = list(Count.objects.filter(location__in=location_objs))
    location_counts = list(Count.objects.filter(asset=asset))
    for count in list(set(location_counts).difference(update_counts)):
        # remove loc association from asset
        count.delete()
        

def assign_asset_fields(asset, update_asset):
    # TODO: is there a way to iterate through these mappings so
    # this does not have to be changed when the model expands?
    asset.description = update_asset.get('description', asset.description)
    asset.original_cost = update_asset.get('original_cost', asset.original_cost)
