from django.db import models
from django.utils import timezone
from django.conf import settings
from problemset.models import Problem


class Contest(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64, unique=True)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField()
    problems = models.ManyToManyField(Problem)

    def __str__(self):
        return self.title
