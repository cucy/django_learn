from django import forms
from django.contrib.auth import authenticate, login, get_user_model, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    """用户注册表单"""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_name', 'email',)  # 'full_name',)

    def clean_password2(self):
        # 检查用户两次输入密码是否正确
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # 密码加盐, 处理
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        # user.is_active = False  # 发送信息到邮箱激活账号信号触发
        # obj = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """ """
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)

        ''' 
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                ## not active, check email activation
                link = reverse("account:resend-activation")
                reconfirm_msg = """Go to <a href='{resend_link}'>
                resend confirmation email</a>.
                """.format(resend_link = link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "检查邮箱进行确认 " + reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " + reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError("This user is inactive.")
        '''
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("验证错误")
        login(request, user)
        self.user = user
        return data


class User_Detail_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = ["password", "last_login"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


class Changge_Password_Form(forms.ModelForm):
    """
      修改密码表单
    """
    error_messages = {
        'password_mismatch': "两次密码不一致",
    }
    old_password = forms.CharField(
        label="旧密码",
        strip=False,
        widget=forms.PasswordInput,
    )

    new_password1 = forms.CharField(
        label="新密码",
        strip=False,
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label="确认新密码",
        strip=False,
        widget=forms.PasswordInput,
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, user=None, *args, **kwargs):
        # 不使用默认的user对象；修改的是别的账号
        self.user = user

        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """

        old_password = self.cleaned_data["old_password"]

        if not self.user.check_password(old_password):
            raise forms.ValidationError("旧密码检查失败")
        return old_password

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class Admin_Changge_Password_Form(forms.ModelForm):
    new_password1 = forms.CharField(
        label="新密码",
        strip=False,
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label="确认新密码",
        strip=False,
        widget=forms.PasswordInput,
    )
    def __init__(self, user=None, *args, **kwargs):
        # 不使用默认的user对象；修改的是别的账号
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


