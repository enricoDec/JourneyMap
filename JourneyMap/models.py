import uuid
import os

from PIL import Image as Img
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Journey model each journey has a user, title and creation date
# Each Journey can have * Image
from WebApplication import settings
from imageAPI.ImageAnalysis import ImageAnalysis

import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)


class Journey(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('JourneyMap_journeys')


class Image(models.Model):
    def upload_image(self, filename):
        return self.journey.user_id.__str__() + '/' + self.journey.id.__str__() + '/' + filename

    def createMaskedUrl(self, filename):
        return

    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, default=None, null=True, blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, default=None, null=True, blank=True)
    date_taken = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_image, null=False, blank=False, unique=True)

    def __str__(self):
        if self.title is not None:
            return self.title.__str__()
        else:
            return self.id.__str__()

    def get_absolute_url(self):
        if self.image.url.startswith('\\media') or self.image.url.startswith('/media'):
            return self.image.url[6:]
        else:
            return self.image.url

    def get_file_path(self):
        return os.path.join(self.journey.user_id.__str__(), self.journey.id.__str__())

    def save(self, *args, **kwargs):
        logging.info(settings.MEDIA_ROOT + '/' + self.get_file_path() + '/' + self.title)
        self.image = os.path.join(self.get_file_path(), self.title)
        image_analysis = ImageAnalysis(settings.MEDIA_ROOT + '/' + self.get_file_path() + '/' + self.title)
        labels = image_analysis.get_minial_exif_label()

        self.latitude = labels['lat']
        self.longitude = labels['long']
        self.date_taken = labels['date']
        super(Image, self).save()

    def delete(self, using=None, keep_parents=False):
        # os.remove(self.image.path)
        super(Image, self).delete()


class CDP(models.Model):
    imageUrl = models.OneToOneField(Image(), on_delete=models.CASCADE)
    # imageUrl = models.FilePathField(Image.get_absolute_url(), unique=True)
    imageMaskUrl = models.UUIDField(unique=True, default=uuid.uuid4)
