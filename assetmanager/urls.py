# -*- coding: utf-8 -*-
from django.urls import path
from assetmanager import views

from rest_framework.urlpatterns import format_suffix_patterns

api_root_path = 'api/v1/'

urlpatterns = [
    path(api_root_path + 'assets/', views.AssetList.as_view(), name="asset-list"),
    path(api_root_path + 'assets/<int:pk>/', views.AssetDetail.as_view(), name="asset-detail"),
    path(api_root_path + 'locations', views.LocationList.as_view(), name="location-list"),
    path(api_root_path, views.api_root),
    
    path('home/', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
    path('about/', views.AboutPageView.as_view(), name='about'),
]

urlpatterns = format_suffix_patterns(urlpatterns)