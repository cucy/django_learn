#!/usr/bin/env python
# _*_ coding:utf8 _*_
from django.urls import path

__date__ = '2018/6/24 22:17'
__author__ = 'zhourudong'

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),

]
