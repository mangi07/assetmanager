# -*- coding: utf-8 -*-
from django.urls import path
from assetmanager import views

from rest_framework.urlpatterns import format_suffix_patterns

api_root_path = 'api/vi/'

urlpatterns = [
    path('', views.api_root), # TODO: change this once home page is created
    path('api/v1/assets/', views.AssetList.as_view(), name="asset-list"),
    path('api/v1/assets/<int:pk>/', views.AssetDetail.as_view(), name="asset-detail"),
    path('api/v1/', views.api_root),
    path(api_root_path + 'locations', views.LocationList.as_view(), name="location-list")
]

urlpatterns = format_suffix_patterns(urlpatterns)