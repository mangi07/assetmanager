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
from rest_framework.renderers import TemplateHTMLRenderer

from django.views.generic import TemplateView

from abc import ABC, abstractmethod
from ..custom_api_exceptions import BadRequestException

# TODO: play around with https://github.com/miki725/django-rest-framework-bulk
# and consider replacing some code with this

class LoginView(TemplateView):
    template_name = "login.html"

class AboutPageView(TemplateView):
    template_name = "about.html"

class HomePageView(TemplateView):
    template_name = "base.html"


class TemplateLoader(APIView):
    """
    A view that returns a templated HTML to load in base.html.
    """

    #from django.template.loader import render_to_string
    #rendered = render_to_string('my_template.html', {'foo': 'bar'})
    renderer_classes = (TemplateHTMLRenderer,)
    #permission_classes = []

    def post(self, request, *args, **kwargs):
        # TODO: parse the url to decide which template to load (more templates to be added)
        template = kwargs.get('template_name')
        template = 'index.html'
        #return Response({'user': self.object}, template_name='index.html')
        return Response(template_name=template)




@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'assets': reverse('asset-list', request=request, format=format),
        'locations': reverse('location-list', request=request, format=format),
        'asset bulk delete': reverse('asset-list-delete', request=request, format=format),
        'location bulk delete': reverse('location-list-delete', request=request, format=format),
        'obtain token pair': reverse('token-obtain-pair', request=request, format=format),
        'obtain token refresh': reverse('token-refresh', request=request, format=format),
        'create user': reverse('create-user', request=request, format=format),
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
        serializer = self.UpdateSerializer(request.user, data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            # need to use the serializer used in get requests
            # for representing data in the response
            id_list = [d['id'] for d in request.data]
            items = self.Item.objects.filter(pk__in=id_list)
            serializer = self.Serializer(items, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ListDelete(ABC, APIView):
    """
    Bulk deletion of items.
    """
    def __init__(self, Item):
        self.Item = Item # must be a django Model
        
    @abstractmethod
    def _validate_post_data(self, request):
        """should return a response if data is invalid"""
        pass
    
    # TODO: this is a workaround because couldn't figure out how to manipulate
    # processing of DELETE request in middelware to keep data,
    # so bulk delete requests have to be made as post requests for now.
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
        
        self._validate_post_data(request)
            
        data = request.data
        
        # all given ids must exist and all or none of them should be deleted
        items = self.Item.objects.filter(pk__in=data)

        if items and len(items) == len(data):
            try:
                items.delete()
            except:
                return Response("Could not delete items.",
                                status.HTTP_400_BAD_REQUEST)
            return Response(data, status.HTTP_200_OK)
        else:
            # give a list of ids that could not be found
            ids = []
            msg = ""
            if items:
                ids = list(set(data).difference([item.id for item in items]))
                msg = "The following IDs could not be found: " + str(ids)
            else:
                msg = "None of the given IDs could be found."
            return Response(msg, status.HTTP_400_BAD_REQUEST)


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
        
    def _validate_post_data(self, request):
        pass


class LocationListDelete(ListDelete):
    def __init__(self):
        super().__init__(Location)
        
    def _validate_post_data(self, request):
        # determine which assets, if any, have any location counts at the given location ids
        ids = request.data
        assets_at_locs = [] # assets containing counts at the given location ids
        locs = []
        msg = ""
        for id in ids:
            assets = Asset.objects.filter(locations__id=id)
            if len(assets) > 0:
                asset_ids = [a.id for a in assets]
                assets_at_locs.extend(asset_ids)
                locs.append(id)
        
        if len(set(assets_at_locs)) > 0:
            msg = ("Could not delete any of the locations because location ids " + str(set(locs)) +
                " are in counts in asset ids " + str(set(assets_at_locs)) + ".")
            raise BadRequestException({"message": msg})

