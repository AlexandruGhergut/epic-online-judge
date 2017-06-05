from django.db import models
from django.utils import timezone
from django.conf import settings
from core import constants
from ckeditor.fields import RichTextField


def source_directory_path(instance, filename):
    return 'user/{0}/problem/{1}/{2}'.format(instance.user.pk,
                                             instance.problem.pk, filename)


def solution_directory_path(instance, filename):
    return 'problem/{0}/solution/{1}'.format(instance.pk, filename)


def testcase_directory_path(instance, filename):
    return 'problem/{0}/tests/{1}'.format(instance.problem.pk, filename)


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    statement = RichTextField()
    input_description = RichTextField()
    output_description = RichTextField()
    publish_datetime = models.DateTimeField(default=timezone.now)
    sample_input = models.CharField(max_length=128)
    sample_output = models.CharField(max_length=128)
    solution_source_file = models.FileField(upload_to=solution_directory_path)
    solution_language = models.IntegerField(choices=constants.Language.CHOICES)
    tags = models.ManyToManyField(Tag, blank=True)


class TestCase(models.Model):
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)
    input_data_file = models.FileField(upload_to=testcase_directory_path)
    output = models.TextField(null=True)
