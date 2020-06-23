from django.forms import ModelForm
from .models import Image
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=100)
    message = forms.CharField(required=True, widget=forms.Textarea, max_length=1000)


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['journey', 'title', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # restrict journeys to current user journeys
        self.fields['journey'].queryset = self.fields['journey'].queryset.filter(user=user)
