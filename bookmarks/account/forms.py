#!/usr/bin/env python
# _*_ coding:utf8 _*_ 
__date__ = '2018/6/25 00:26'
__author__ = 'zhourudong'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
