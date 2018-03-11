from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
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
