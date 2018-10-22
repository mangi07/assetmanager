from rest_framework.parsers import JSONParser
from assetmanager.models import Asset
from assetmanager.serializers import AssetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class AssetList(APIView):
    """
    List all assets, or create a new asset.
    """
    def get(self, request, format=None):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if not request.body:
            return Response("no data", status.HTTP_400_BAD_REQUEST)
        data = JSONParser().parse(request)
        serializer = AssetSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# TODO: test/refactor this
class AssetDetail(APIView):
    """
    Retrieve, update or delete an asset.
    """
    def get_object(self, pk):
        try:
            return Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        asset = self.get_object(pk)
        serializer = AssetSerializer(asset)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        data = JSONParser().parse(request)
        asset = self.get_object(pk)
        serializer = AssetSerializer(asset, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        asset = self.get_object(pk)
        asset.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    
