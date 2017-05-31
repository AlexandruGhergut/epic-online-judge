from django.db.models.functions import Now
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import ProblemForm, SubmissionForm, TestCaseForm
from .models import Problem, Submission
from .tasks import judge_submission


class CreateProblemView(LoginRequiredMixin, CreateView):
    form_class = ProblemForm
    template_name = "problemset/create_problem.html"
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        test_case_form = TestCaseForm()

        return self.render_to_response(
            self.get_context_data(form=form,
                                  test_case_form=test_case_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        test_case_form = TestCaseForm(self.request.POST,
                                      self.request.FILES)

        if (form.is_valid() and test_case_form.is_valid()):
            form.instance.user = self.request.user

            self.object = form.save(commit=False)
            test_case = test_case_form.save(commit=False)

            self.object.test_case = test_case
            self.object.save()  # save problem object

            test_case.problem = self.object
            test_case.save()  # save test object

            return HttpResponseRedirect(self.get_success_url())

        return self.render_to_response(
            self.get_context_data(form=form,
                                  test_case_form=test_case_form)
        )


class ListProblemsView(ListView):
    template_name = 'problemset/list_problems.html'
    queryset = Problem.objects.filter(publish_datetime__lte=Now()) \
        .order_by('-publish_datetime')


class DetailProblemView(DetailView):
    model = Problem
    template_name = 'problemset/view_problem.html'

    def get_context_data(self, **kwargs):
        context = super(DetailProblemView, self).get_context_data(**kwargs)
        submission_form = SubmissionForm()
        context['submission_form'] = submission_form
        return context

    # Request for source submission
    def post(self, request, *args, **kwargs):
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem = self.get_object()
            submission.language = 0
            submission.save()

            judge_submission.delay(submission.pk)
            return HttpResponseRedirect('{0}?user={1}&problem={2}'.format(
                reverse('problemset:list_submissions'),
                request.user.pk,
                submission.problem.pk
            ))


class ListSubmissionView(ListView):
    model = Submission
    template_name = 'problemset/list_submissions.html'

    def get_queryset(self):
        fields = ('user', 'problem')
        query_dict = {}
        for field in fields:
            value = self.request.GET.get(field)
            if value:
                query_dict[field] = value

        return Submission.objects.filter(**query_dict)


class SourceView(View):
    def get(self, request, pk, *args, **kwargs):
        submission = get_object_or_404(Submission, pk=pk)
        source_field = submission.source_file
        content = source_field.storage.open(source_field.name).read()
        return render(request, 'problemset/view_source.html',
                      {'source': content})
