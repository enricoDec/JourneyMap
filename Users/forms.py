from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegister(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField()
    surname = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'email', 'password1', 'password2']
