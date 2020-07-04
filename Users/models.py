import uuid

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)

    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics', null=False, blank=False)

    def __str__(self):
        return f'{self.user} Profile'

    # noinspection TryExceptPass
    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(user_id=self.user_id)
            if this.image != self.image and this.image.url != '/media/profile_pics/default.jpg':
                default_storage.delete(this.image.path)
        except:
            pass

        super(Profile, self).save()
        image = Image.open(self.image.path)

        # Resize Profile Pic if too big
        # Temp solution
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)
