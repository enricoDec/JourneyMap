from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Journey(models.Model):
    # id = models.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.FileField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
