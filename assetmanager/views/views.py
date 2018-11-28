from assetmanager.models import Asset, Location
from assetmanager.serializers import AssetSerializer, LocationSerializer, LocationUpdateSerializer
#from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
#from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

#from django_filters.rest_framework import DjangoFilterBackend
from ..filters import LocationFilter

import json

# TODO: play around with https://github.com/miki725/django-rest-framework-bulk
# and consider replacing some code with this


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'assets': reverse('asset-list', request=request, format=format),
        'locations': reverse('location-list', request=request, format=format),
    })


class AssetList(APIView):
    """
    List all assets, or create one or more new assets.
    """
    def get(self, request, format=None):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if not request.data:
            return Response("no data", status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer = AssetSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AssetDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    

class LocationList(APIView):
    """
    Bulk CRUD on locations
    """
    def get(self, request, format=None):
        params = self.request.query_params # returns {"param1":"val1",...}
        locations = Location.objects.all()
        locations_filter = LocationFilter(locations, params)
        serializer = LocationSerializer(locations_filter.qs(), many=True)
        #serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if not request.data:
            return Response("no data given in request", status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer = LocationSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request, format=None):
        if not request.data:
            return Response("no data given in request", status.HTTP_400_BAD_REQUEST)
        
        data = request.data
        serializer = LocationUpdateSerializer(data=data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        if not request.data:
            return Response("no data given in request", status.HTTP_400_BAD_REQUEST)
        data = request.data
        
        # all given ids must exist and all or none of them should be deleted
        locations = Location.objects.filter(pk__in=data)
        if locations and len(locations) == len(data):
            try:
                locations.delete()
            except:
                return Response("Could not delete locations.",
                                status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data, status.HTTP_200_OK)
        else:
            return Response("One or more of the given location ids could not be found.",
                           status.HTTP_400_BAD_REQUEST)
             
            
            
            
        