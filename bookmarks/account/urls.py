#!/usr/bin/env python
# _*_ coding:utf8 _*_ 
__date__ = '2018/6/25 00:28'
__author__ = 'zhourudong'

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # login views
    # path('login/', views.user_login, name='login'),

    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form1.html"),
         name='password_change', ),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done1.html"),
         name='password_change_done'),
]
