#!/usr/bin/env python
# _*_ coding:utf8 _*_
from django.contrib.auth.models import User

__date__ = '2018/6/25 00:26'
__author__ = 'zhourudong'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """用户注册"""
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次密码不一致.')
        return cd['password2']
