from django.db import models
from django.utils import timezone
from django.conf import settings


class Contest(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64, unique=True)
    start_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
