from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserRegister(UserCreationForm):
    email = forms.EmailField(label=_(u'Email'), help_text=_(u'Please enter a valid Email'))
    name = forms.CharField(label=_(u'Name'))
    surname = forms.CharField(label=_(u'Surname'))

    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'email', 'password1', 'password2']
