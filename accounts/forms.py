from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import User


class CaseInsensitiveUsernameMixin(forms.Form):
    """
    Disallow a username with a case-insensitive match of existing usernames.
    """

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username__iexact=username) \
                .exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_(u'The username ‘{}’ is already in use.'.format(str(username).casefold())))
        return username


class RegisterForm(UserCreationForm, CaseInsensitiveUsernameMixin):
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
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'autofocus': 'True'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserInfoForm(ModelForm, CaseInsensitiveUsernameMixin):
    """
    User info form. Used with user_info view and template
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
