#!/usr/bin/env python
# _*_ coding:utf8 _*_
from django.db.models import Q

__date__ = '2018/6/25 01:52'
__author__ = 'zhourudong'

from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    Authenticate using an e-mail address.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(email=username)|Q(username=username))
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
