from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _


class UserRegister(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField()
    surname = forms.CharField()

    class Meta:
        model = User
        fields = ['username', _('name'), _('surname'), _('email'), 'password1', 'password2']
