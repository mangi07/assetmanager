# -*- coding: utf-8 -*-
from django.urls import path
from assetmanager import views

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_root_path = 'api/v1/'

urlpatterns = [
    # protected views - authentication should be required
    path(api_root_path + 'assets/', views.AssetList.as_view(), name="asset-list"),
    path(api_root_path + 'assets/<int:pk>/', views.AssetDetail.as_view(), name="asset-detail"),
    path(api_root_path + 'locations', views.LocationList.as_view(), name="location-list"),
    path(api_root_path, views.api_root),
    
    path(api_root_path + 'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(api_root_path + 'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # todo - protect this page !!
    path('home/', views.HomePageView.as_view(), name='home'),
    
    
    # public views - no authentication required
    path('login/', views.LoginView.as_view(), name='login'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)