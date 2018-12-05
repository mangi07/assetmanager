# -*- coding: utf-8 -*-
from rest_framework.settings import api_settings


class CustomPaginator:
    # borrowed from https://stackoverflow.com/questions/35830779/django-rest-framework-apiview-pagination
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
                self._paginator.ordering = ["-created", "id"]
        return self._paginator
    
    def paginate_queryset(self, queryset):
         """
         Return a single page of results, or `None` if pagination is disabled.
         """
         if self.paginator is None:
             return None
         return self.paginator.paginate_queryset(queryset, self.request, view=self)
     
    def get_paginated_response(self, serializer_class, query_set):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        page = self.paginate_queryset(query_set)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.paginator.get_paginated_response(serializer.data)
        return None