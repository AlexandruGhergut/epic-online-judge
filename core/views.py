from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Submission
from problemset.models import Problem
from .forms import SubmissionForm
from .tasks import judge_submission


class IndexView(View):
    def get(self, request):
        return render(request, 'core/index.html')


class ListSubmissionView(ListView):
    model = Submission
    template_name = 'core/list_submissions.html'

    def get_queryset(self):
        fields = ('user', 'problem')
        query_dict = {}
        for field in fields:
            value = self.request.GET.get(field)
            if value:
                query_dict[field] = value

        return Submission.objects.filter(**query_dict).order_by('-datetime')


class SourceView(View):
    def get(self, request, pk, *args, **kwargs):
        submission = get_object_or_404(Submission, pk=pk)
        source_field = submission.source_file
        content = source_field.storage.open(source_field.name).read()
        return render(request, 'core/view_source.html',
                      {'source': content})


class SourceSubmitView(View):
    def post(self, request, pk, *args, **kwargs):
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = \
                get_object_or_404(Problem, pk=pk)
            submission.save()

            judge_submission.delay(submission.pk)
            return HttpResponseRedirect('{0}?user={1}&problem={2}'.format(
                reverse('core:list_submissions'),
                request.user.pk,
                submission.problem.pk
            ))
