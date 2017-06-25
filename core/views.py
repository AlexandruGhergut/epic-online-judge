from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from blog.models import Post
from .models import Submission
from problemset.models import Problem
from .forms import SubmissionForm
from .tasks import dispatch_submission


class IndexView(View):
    def get(self, request):
        posts = Post.objects.filter(on_homepage=True)

        context = {'posts': posts}
        return render(request, 'core/index.html', context)


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

        source_file = submission.source_file
        source_file = source_file.storage.open(source_file.name)
        source_content = source_file.read()

        solution_output = submission.problem.testcase.output

        test_file = submission.problem.testcase.input_data_file
        test_file = test_file.storage.open(test_file.name)
        test_content = test_file.read()

        source_output = submission.source_output

        context = {'source_content': source_content,
                   'test_content': test_content,
                   'source_output': source_output,
                   'solution_output': solution_output}

        source_file.close()
        test_file.close()
        return render(request, 'core/view_source.html', context)


class SourceSubmitView(View):
    def post(self, request, pk, *args, **kwargs):
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = \
                get_object_or_404(Problem, pk=pk)
            submission.save()

            dispatch_submission.delay(submission.pk)
            return HttpResponseRedirect('{0}?user={1}&problem={2}'.format(
                reverse('core:list_submissions'),
                request.user.pk,
                submission.problem.pk
            ))


class GetSubmissionStatusView(View):
    def post(self, request):
        ids = request.POST.getlist('ids[]')

        status_dict = {}
        submissions = Submission.objects.filter(pk__in=ids)

        for submission in submissions:
            status_dict[submission.pk] = submission.get_status_display()

        return JsonResponse(status_dict)
