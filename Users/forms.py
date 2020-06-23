from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import ugettext_lazy as _

from .models import Profile


class UserRegister(UserCreationForm):
    email = forms.EmailField(max_length=150, label=_(u'Email'), help_text=_(u'Please enter a valid Email'))
    first_name = forms.CharField(max_length=40, label=_(u'Name'))
    last_name = forms.CharField(max_length=254, label=_(u'Surname'))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserLogin(AuthenticationForm):
    username = UsernameField(label=_('Username or Email'), widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
