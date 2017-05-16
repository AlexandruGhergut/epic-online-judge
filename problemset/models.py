from django.db import models
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField


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


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_file = models.FileField(upload_to=testcase_directory_path)
    output_file = models.FileField(upload_to=testcase_directory_path)


class SubmissionError(models.Model):
    description = models.IntegerField()


class Submission(models.Model):
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Success'),
        (2, 'Error'),
    )
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    source_file = models.FileField(upload_to=source_directory_path)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    error = models.OneToOneField(SubmissionError, null=True)
    score = models.IntegerField(null=True)
