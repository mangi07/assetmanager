# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from .custom_api_exceptions import BadRequestException

class BaseFilter(ABC):
    """Override to create custom filters"""
    def __init__(self, locations, params):
        self.locations = locations
        self.params = params
    
    @abstractmethod
    def _filter(self, key, value, queryset):
        pass
        
    def qs(self):
        """get filtered queryset using params"""
        # params {"param1":"val1",...}
        for k,v in self.params.items():
            self.locations = self._filter(k, v, self.locations)
                
        return self.locations
    

class LocationFilter(BaseFilter):
    """Allows complete customization of querystring filtering."""
    # add to this if-else chain to expand filtering options
    def _filter(self, key, value, queryset):
        if key == "id":
            try:
                return queryset.filter(id=int(value))
            except:
                return []
        elif key == "description":
            return queryset.filter(description=value)
        elif key == "description__like":  # leaning towards sql syntax LIKE
            return queryset.filter(description__contains=value)
        elif key == "cursor":
            return queryset # Allow for pagination
        else:
            raise BadRequestException("Could not use one or more provided filters.")
            

class AssetFilter(BaseFilter):
    """Allows complete customization of querystring filtering."""
    # add to this if-else chain to expand filtering options
    def _filter(self, key, value, queryset):
        if key == "id":
            try:
                return queryset.filter(id=int(value))
            except:
                return []
        elif key == "description":
            return queryset.filter(description=value)
        elif key == "description__like":  # leaning towards sql syntax LIKE
            return queryset.filter(description__contains=value)
        elif key == "original_cost":
            return queryset.filter(original_cost=value)
        elif key == "original_cost__lt":
            return queryset.filter(original_cost__lt=value)
        elif key == "original_cost__gt":
            return queryset.filter(original_cost__gt=value)
        elif key == "location":
            return queryset.filter(count__location__description=value)
        elif key == "cursor":
            return queryset # Allow for pagination
        else:
            raise BadRequestException("Could not use one or more provided filters.")
        