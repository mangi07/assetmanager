# -*- coding: utf-8 -*-
from django.urls import path
from assetmanager import views

urlpatterns = [
    path('assets/', views.AssetList.as_view(), name="asset-list"),
    path('assets/<int:pk>/', views.AssetDetail.as_view(), name="asset-detail"),
]