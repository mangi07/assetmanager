# -*- coding: utf-8 -*-
from django.urls import path
from assetmanager import views

urlpatterns = [
    path('assets/', views.asset_list),
    path('assets/<int:pk>/', views.asset_detail),
]