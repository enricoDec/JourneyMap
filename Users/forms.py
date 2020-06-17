from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _


class UserRegister(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=254)

    class Meta:
        model = User
        fields = ['username', _('first_name'), _('last_name'), _('email'), 'password1', 'password2']
