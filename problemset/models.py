from django.db import models
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField
from . import constants

def solution_directory_path(instance, filename):
    return 'problem/{0}/solution/{1}'.format(instance.pk, filename)


def testcase_directory_path(instance, filename):
    return 'problem/{0}/tests/{1}'.format(instance.problem.pk, filename)


def source_directory_path(instance, filename):
    return 'user/{0}/problem/{1}/{2}'.format(instance.user.pk,
                                             instance.problem.pk, filename)


class Problem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    statement = RichTextField()
    publish_datetime = models.DateTimeField(default=timezone.now)
    sample_input = models.CharField(max_length=128)
    sample_output = models.CharField(max_length=128)
    solution_source_file = models.FileField(upload_to=solution_directory_path)


class TestCase(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    input_data_file = models.FileField(upload_to=testcase_directory_path)


class SubmissionError(models.Model):
    description = models.IntegerField()


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    source_file = models.FileField(upload_to=source_directory_path)
    status = models.IntegerField(default=0, choices=constants.Status.CHOICES)
    error = models.OneToOneField(SubmissionError, null=True)
    language = models.IntegerField(choices=constants.Language.CHOICES)
