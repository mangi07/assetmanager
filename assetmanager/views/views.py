from assetmanager.models import Asset, Location
from assetmanager.serializers import AssetSerializer, LocationSerializer
#from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
#from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


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
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if not request.data:
            return Response("no data", status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer = LocationSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):
        if not request.data:
            return Response("no data", status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer = LocationSerializer(data=data, many=True)
        if serializer.is_valid():
            print(serializer.data())
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    