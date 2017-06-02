from django.db import models
from django.conf import settings
from django.utils import timezone
from problemset.models import Problem
from . import constants


def source_directory_path(instance, filename):
    return 'user/{0}/problem/{1}/{2}'.format(instance.user.pk,
                                             instance.problem.pk, filename)


class SubmissionError(models.Model):
    description = models.IntegerField()


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    source_file = models.FileField(upload_to=source_directory_path)
    status = models.IntegerField(default=constants.Status.PENDING,
                                 choices=constants.Status.CHOICES)
    error = models.OneToOneField(SubmissionError, null=True)
    language = models.IntegerField(choices=constants.Language.CHOICES)
    datetime = models.DateTimeField(default=timezone.now)
