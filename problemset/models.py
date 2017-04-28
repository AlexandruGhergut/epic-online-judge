from django.db import models
from django.utils import timezone
from django.conf import settings


class Problem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    statement = models.TextField()
    publish_datetime = models.DateTimeField(default=timezone.now)
