import uuid

from PIL import Image as Img
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone


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
    def upload_image(self, filename):
        return 'journeys/' + self.journey.user_id.__str__() + '/' + filename

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
        return reverse('JourneyMap_journeys')

    def save(self, *args, **kwargs):
        super(Image, self).save()
        image = Img.open(self.image.path)

        # Resize Profile Pic if too big
        if image.height > 1920 or image.width > 1080:
            output_size = (1920, 1080)
            image.thumbnail(output_size)
            image.save(self.image.path)

    def delete(self, using=None, keep_parents=False):
        # os.remove(self.image.path)
        super(Image, self).delete()


class CDP(models.Model):
    imageUrl = models.OneToOneField(Image(), on_delete=models.CASCADE)
    # imageUrl = models.FilePathField(Image.get_absolute_url(), unique=True)
    imageMaskUrl = models.UUIDField(unique=True, default=uuid.uuid4)
