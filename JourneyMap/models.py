from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from imageAPI.ImageAnalysis import ImageAnalysis


# Journey model each journey has a user, title and creation date
# Each Journey can have * Image


class Journey(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('JourneyMap_journeys')


class Image(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, default=None, null=True, blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, default=None, null=True, blank=True)
    date_taken = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='journey_images/', null=False, blank=False)

    def __str__(self):
        if self.title is not None:
            return self.title.__str__()
        else:
            return self.id.__str__()

    def get_absolute_url(self):
        return reverse('JourneyMap_journeys')

    def save(self, *args, **kwargs):
        image_analysis = ImageAnalysis(self.image)
        labels = image_analysis.get_minial_exif_label()

        self.latitude = labels['lat']
        self.longitude = labels['long']
        self.date_taken = labels['date']
        super(Image, self).save()

