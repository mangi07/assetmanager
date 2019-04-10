from assetmanager.models import Asset, Location
from assetmanager.serializers import (
    AssetSerializer,
    AssetUpdateSerializer,
    LocationSerializer,
    LocationUpdateSerializer)
#from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
#from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

#from django_filters.rest_framework import DjangoFilterBackend
from ..filters import LocationFilter, AssetFilter
from .custom_paginator import CustomPaginator

from ..tests.schemas.utils import load_json_schema
from jsonschema import validate
from jsonschema import ValidationError

from django.views.generic import TemplateView

# TODO: play around with https://github.com/miki725/django-rest-framework-bulk
# and consider replacing some code with this

class LoginView(TemplateView):
    template_name = "login.html"


class HomePageView(TemplateView):
    template_name = "index.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'assets': reverse('asset-list', request=request, format=format),
        'locations': reverse('location-list', request=request, format=format),
        'asset bulk delete': reverse('asset-list-delete', request=request, format=format),
    })
    
class CustomBulkAPIView(CustomPaginator, APIView):
    """
    Bulk CRUD on locations
    """
    def __init__(self, Item, ItemFilter, Serializer, UpdateSerializer):
        self.Item = Item # must be a django Model
        self.ItemFilter = ItemFilter # must be a BaseFilter from filters.py
        self.Serializer = Serializer # must be a django ModelSerializer
        self.UpdateSerializer = UpdateSerializer # must be a custom UpdateSerializer from serializers.py
    
    # TODO: test pagination and filtering
    # TODO: order locations by their location nesting
    def get(self, request, format=None):
        params = self.request.query_params # returns {"param1":"val1",...}
        items = self.Item.objects.all()
        item_filter = self.ItemFilter(items, params)
        paginated_data = self.get_paginated_response(self.Serializer, item_filter.qs())
        if paginated_data:
            return paginated_data
        data = self.Serializer(item_filter.qs()).data
        return Response(data, many=True)
    
    
    def post(self, request, format=None):
        """bulk creation or deletion of items given in list"""
        if not request.data:
            return Response("no data given in request", status.HTTP_400_BAD_REQUEST)
        
        # TODO: this is a workaround because couldn't figure out how to manipulate
        # processing of DELETE request in middelware to keep data,
        # so bulk delete requests have to be made as post requests for now.
        # TODO: if request post schema for bulk update doesn't validate and 'delete' in data,
        #   call delete function, else raise an error.
        if True and 'delete' in request.data:
            return self.delete(request)
        
        data = request.data
        serializer = self.Serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, format=None):
        """bulk update of items given in list"""
        if not request.data:
            return Response("no data given in request", status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        serializer = self.UpdateSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            # need to use the serializer used in get requests
            # for representing data in the response
            id_list = [d['id'] for d in request.data]
            items = self.Item.objects.filter(pk__in=id_list)
            serializer = self.Serializer(items, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, format=None):
        if not request.data:
            return Response("no data given in request", status.HTTP_400_BAD_REQUEST)
        
        m_err_msg = '.  Expected list of ids to delete: eg: {"delete":[1,2,3]}'
        json_schema = load_json_schema("asset_list_delete.json")
        try:
            validate(request.data, json_schema)
        except ValidationError as err:
            msg = err.message + m_err_msg
            return Response(msg, status.HTTP_400_BAD_REQUEST)
        
        if (
                not 'delete' in request.data or
                type(request.data['delete']) != list or
                False in [(lambda id: type(id)==int)(id)
                    for id in request.data['delete']]
            ):
            return Response(m_err_msg, status.HTTP_400_BAD_REQUEST)
            
        data = request.data['delete']
        
        # all given ids must exist and all or none of them should be deleted
        items = self.Item.objects.filter(pk__in=data)

        if items and len(items) == len(data):
            try:
                items.delete()
            except:
                return Response("Could not delete items.",
                                status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data, status.HTTP_200_OK)
        else:
            return Response("One or more of the given item ids could not be found.",
                           status.HTTP_400_BAD_REQUEST)


# TODO: api view to bulk remove asset-location associations
class ListDelete(APIView):
    """
    Bulk CRUD on locations
    """
    def __init__(self, Item):
        self.Item = Item # must be a django Model
    
    def post(self, request, format=None):
        if not request.data:
            return Response("no data given in request", status.HTTP_400_BAD_REQUEST)
        
        m_err_msg = '.  Expected list of ids to delete: eg: [1,2,3]'
        json_schema = load_json_schema("list_delete.json")
        try:
            validate(request.data, json_schema)
        except ValidationError as err:
            msg = err.message + m_err_msg
            return Response(msg, status.HTTP_400_BAD_REQUEST)
        
        if (
                type(request.data) != list or
                False in [(lambda id: type(id)==int)(id)
                    for id in request.data]
            ):
            return Response(m_err_msg, status.HTTP_400_BAD_REQUEST)
            
        data = request.data
        
        # all given ids must exist and all or none of them should be deleted
        # TODO: maybe look into making this an atomic transaction
        items = self.Item.objects.filter(pk__in=data)

        if items and len(items) == len(data):
            try:
                items.delete()
            except:
                return Response("Could not delete items.",
                                status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data, status.HTTP_200_OK)
        else:
            # TODO: give a more specific response, stating a list of ids that could not be found
            return Response("One or more of the given item ids could not be found.",
                           status.HTTP_400_BAD_REQUEST)


class AssetDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    

class LocationList(CustomBulkAPIView):
    def __init__(self):
        super().__init__(Location,
            LocationFilter,
            LocationSerializer,
            LocationUpdateSerializer)


class AssetList(CustomBulkAPIView):
    def __init__(self):
        super().__init__(Asset,
            AssetFilter,
            AssetSerializer,
            AssetUpdateSerializer)


class AssetListDelete(ListDelete):
    def __init__(self):
        super().__init__(Asset)




