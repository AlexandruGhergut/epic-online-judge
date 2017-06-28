from django.db import models
from django.conf import settings
from django.utils import timezone
from problemset.models import Problem
from contest.models import Contest
from . import constants


def source_directory_path(instance, filename):
    return 'user/{0}/submission/{1}/{2}'.format(instance.user.pk,
                                                instance.pk, filename)


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
    source_output = models.TextField(null=True)
    contest = models.ForeignKey(Contest, default=None, null=True, blank=True)

    def __str__(self):
        return '(' + str(self.pk) + ', ' + str(self.user) + ')'
