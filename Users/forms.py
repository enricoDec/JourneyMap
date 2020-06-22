from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class UserRegister(UserCreationForm):
    email = forms.EmailField(label=_(u'Email'), help_text=_(u'Please enter a valid Email'))
    first_name = forms.CharField(max_length=40, label=_(u'Name'))
    last_name = forms.CharField(max_length=254, label=_(u'Surname'))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
