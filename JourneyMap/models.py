from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image as img


# Journey model each journey has a user, title and creation date
# Each Journey can have * Image


class Journey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('JourneyMap_journeys')


# TODO: ID not auto increment
# Each image corresponds to a Journey
# Image has all the metadata and file path to the image
class Image(models.Model):
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, default=None, null=True, blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=15, default=None, null=True, blank=True)
    date_taken = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='journey_images/', null=False, blank=False)

    def __str__(self):
        if self.title is not None:
            return self.title.__str__()
        else:
            return self.id.__str__()

    def get_absolute_url(self):
        return reverse('JourneyMap_journeys')

    def save(self, *args, **kwargs):
        super(Image, self).save()
        image = img.open(self.image.path)

        # Resize Profile Pic if too big
        if image.height > 1920 or image.width > 1080:
            output_size = (1920, 1080)
            image.thumbnail(output_size)
            image.save(self.image.path)

