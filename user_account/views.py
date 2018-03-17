from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, DetailView, UpdateView, ListView
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404, JsonResponse, HttpResponse
from django.forms.models import model_to_dict

from .forms import UserRegisterForm, LoginForm, User_Detail_Form, Changge_Password_Form, Admin_Changge_Password_Form
from .models import User


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = 'index.html'


class RegisterView(CreateView):
    """用户注册视图"""
    form_class = UserRegisterForm
    template_name = 'user_account/user_register.html'
    success_url = reverse_lazy("login")


class LoginView(FormView):
    """用户登录视图"""
    form_class = LoginForm
    template_name = 'user_account/user_login.html'
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


def logout_fun(request):
    """ 用户退出函数 """
    if not request.user.is_authenticated:
        return render(request, 'user_account/user_login.html')

    logout(request)
    return render(request, 'user_account/user_login.html')


class User_Detail_View(LoginRequiredMixin, UpdateView):
    """
    用户详情页，修改个人信息以及密码     , bug 修改别人账号风险
    """
    template_name = 'user_account/user_detail_setting.html'
    ajax_form_template_name = "user_account/snippets/change_user_info.html"
    context_object_name = 'user_obj'
    form_class = User_Detail_Form
    model = User

    def get_template_names(self):
        if self.request.GET.get('ic-request') or self.request.POST.get('ic-request'):
            """ 修改用户信息获取 是ic-request 则更改默认模板 """
            self.template_name = self.ajax_form_template_name
        return super().get_template_names()

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        if pk:
            pk = int(pk)
        if self.request.user.pk != pk and not self.request.user.is_admin:
            raise Http404("没有该用户")
        return get_object_or_404(User, pk=pk)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if not form.is_valid():
            """ 返回ajax form如果检查未通过"""
            self.template_name = self.ajax_form_template_name
            return super(User_Detail_View, self).post(request, *args, **kwargs)
        else:
            self.object = form.save(True)
            from django.http import HttpResponse

            # data = {"message": self.object.email}
            # import json
            # data = json.dumps(data)
            # return HttpResponse(content=data, status=202, )
            return HttpResponse(status=202, )


class User_List_View(ListView):
    model = User
    template_name = 'user_account/user_list.html'
    context_object_name = "user_obj_list"


class Changge_Password_View(UpdateView):
    """ 修改密码视图"""
    form_class = Changge_Password_Form
    template_name = 'user_account/user_change_password.html'
    model = User
    context_object_name = 'user_obj'

    def get_success_url(self):
        """ 修改密码成功， 返回用户详情页"""
        pk = {"pk": self.kwargs.get('pk')}
        url = reverse_lazy('user_detail', kwargs=pk)
        return url

    def get_form_class(self):
        """ 当前登录的用户是管理员；则不需要验证旧密码"""
        if self.request.user.is_admin:
            return Admin_Changge_Password_Form
        return super().get_form_class()

    def get_form_kwargs(self):
        pk = self.kwargs.get('pk')
        kwargs = super().get_form_kwargs()

        #  传入特定的用户模型
        kwargs['user'] = get_object_or_404(User, pk=pk)
        return kwargs


class User_Info_View(View):
    def get(self, request):
        return render(request, 'test.html')
