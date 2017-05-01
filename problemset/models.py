from django.db import models
from django.utils import timezone
from django.conf import settings


def testcase_directory_path(instance, filename):
    return 'problem/{0}/tests/filename'.format(instance.problem.pk)


class Problem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    statement = models.TextField()
    publish_datetime = models.DateTimeField(default=timezone.now)


class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_file = models.FileField(upload_to=testcase_directory_path)
    output_file = models.FileField(upload_to=testcase_directory_path)
