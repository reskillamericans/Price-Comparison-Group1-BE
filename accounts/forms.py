from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    """
    User registration form. Used with register view and template
    """
    # id templates for css customization
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ['username', 'email',
                  'first_name', 'last_name', 'password1', 'password2']


class LoginForm(forms.Form):
    """
    User login form. Used with login view and template
    """
    username = forms.CharField(label='Username', max_length=100, )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserInfoForm(ModelForm):
    """
    User info form. Used with user_info view and template
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
