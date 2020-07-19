from django.forms import ModelForm
from .models import Image, Journey
from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label=_(u'Name'), max_length=100)
    email = forms.EmailField(required=True, label=_(u'Email'), max_length=100)
    message = forms.CharField(required=True, label=_(u'Message'), widget=forms.Textarea, max_length=1000, min_length=12)


class AddJourneyForm(ModelForm):
    class Meta:
        model = Journey
        fields = ['title']


class DeleteJourneyForm(ModelForm):
    class Meta:
        model = Journey
        fields = ['id']


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['journey', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # restrict journeys to current user journeys
        #self.fields['journey'].queryset = self.fields['journey'].queryset.filter(user=user)
