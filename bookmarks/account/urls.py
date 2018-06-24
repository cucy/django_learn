#!/usr/bin/env python
# _*_ coding:utf8 _*_ 
__date__ = '2018/6/25 00:28'
__author__ = 'zhourudong'

from django.urls import path
from . import views

urlpatterns = [
    # login views
    path('login/', views.user_login, name='login'),
]
