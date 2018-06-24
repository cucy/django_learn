#!/usr/bin/env python
# _*_ coding:utf8 _*_ 
__date__ = '2018/6/25 02:13'
__author__ = 'zhourudong'

from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
]
