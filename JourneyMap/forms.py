from django.forms import ModelForm
from .models import Image


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['journey', 'title', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # restrict journeys to current user journeys
        self.fields['journey'].queryset = self.fields['journey'].queryset.filter(user=user)
