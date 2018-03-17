"""djuser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.views.generic import TemplateView
from user_account.views import (RegisterView, LoginView, IndexView, User_Detail_View, logout_fun, Changge_Password_View,
                                User_List_View)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r"^$", IndexView.as_view(), name="index"),

    url(r"^user/register/$", RegisterView.as_view(), name="register"),
    url(r"^user/login/$", LoginView.as_view(), name="login"),
    url(r"^user/detail/(?P<pk>\d+)/$", User_Detail_View.as_view(), name="user_detail"),
    url(r"^user/changepass/(?P<pk>\d+)/$", Changge_Password_View.as_view(), name="user_change_password"),
    url(r"^user/list/$", User_List_View.as_view(), name="user_list"),
    url(r"^user/logout/$", logout_fun, name="logout"),

    url(r'^test/$', TemplateView.as_view(template_name='test.html'), name='test')

]
