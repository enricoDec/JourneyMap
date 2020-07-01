from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label=_(u'Name'), max_length=100)
    email = forms.EmailField(required=True, label=_(u'Email'), max_length=100)
    message = forms.CharField(required=True, label=_(u'Message'), widget=forms.Textarea, max_length=1000, min_length=12)
