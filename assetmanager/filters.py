# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
import django_filters
from .custom_api_exceptions import BadRequestException

class LocationFilter:
    """Allows complete customization of querystring filtering."""
    
    def __init__(self, locations, params):
        self.locations = locations
        self.params = params
    

    # add to this if-else chain to expand filtering options
    def _filter(self, key, value, queryset):
        if key == "id":
            try:
                return queryset.filter(id=int(value))
            except:
                return []
        elif key == "description":
            return queryset.filter(description=value)
        elif key == "description_like":  # leaning towards sql syntax LIKE
            return queryset.filter(description__contains=value)
        else:
            raise BadRequestException("Could not use one or more provided filters.")
        
        
    def qs(self):
        """get filtered queryset using params"""
        # params {"param1":"val1",...}
        for k,v in self.params.items():
            self.locations = self._filter(k, v, self.locations)
                
        return self.locations