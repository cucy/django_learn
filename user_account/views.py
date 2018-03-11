from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from django.contrib.auth.views import LoginView  as aa

from .forms import UserRegisterForm, LoginForm


class RegisterView(CreateView):
    """用户注册视图"""
    form_class = UserRegisterForm
    template_name = 'user_account/user_register.html'
    success_url = reverse_lazy("login")


# class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
#     form_class = LoginForm
#     success_url = '/'
#     template_name = 'accounts/login.html'
#     default_next = '/'
#
#     def form_valid(self, form):
#         next_path = self.get_next_url()
#         return redirect(next_path)


class LoginView(FormView):
    """用户登录视图"""
    form_class = LoginForm
    template_name = 'user_account/user_login.html'
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
