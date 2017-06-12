from django.contrib import admin
from .models import SubmissionError, Submission


admin.site.register(Submission)
admin.site.register(SubmissionError)
