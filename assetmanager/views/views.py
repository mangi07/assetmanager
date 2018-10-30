from assetmanager.models import Asset
from assetmanager.serializers import AssetSerializer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics



class AssetList(APIView):
    """
    List all assets, or create one or more new assets.
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


class AssetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer