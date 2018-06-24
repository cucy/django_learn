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
    path('login/', auth_views.LoginView.as_view(template_name="registration/login1.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name="registration/password_change_form1.html"),
         name='password_change', ),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done1.html"),
         name='password_change_done'),

    #  修改密码
    path('password_reset/',  # 重置密码页面
         auth_views.PasswordResetView.as_view(
             template_name="registration/password_reset_form1.html",
             email_template_name="registration/password_reset_email1.html"
         ),
         name='password_reset'),
    path('password_reset/done/',  # 发送邮件成功后显示的页面
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done1.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',  # 邮件链接跳转到此页面
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm1.html"),
         name='password_reset_confirm'),
    path('reset/done/',  # 修改密码成功页面
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete1.html"),
         name='password_reset_complete'),
    # 注册
    path('register/', views.register, name='register'),

    # 扩展用户模型
    path('edit/', views.edit, name='edit'),

]
