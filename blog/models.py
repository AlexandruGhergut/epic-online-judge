from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField


class Post(models.Model):
    class Meta:
        permissions = (
            ("can_post_on_homepage", "Can post on homepage"),
        )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = RichTextField()
    datetime = models.DateTimeField(default=timezone.now)
    on_homepage = models.BooleanField(default=False)
