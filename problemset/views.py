import json
from django.db.models.functions import Now
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from core.forms import SubmissionForm
from .forms import ProblemForm, TestCaseForm
from .models import Problem, Tag
from .tasks import judge_problem_solution


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
        print(request.POST)
        if (form.is_valid() and test_case_form.is_valid()):
            form.instance.user = self.request.user

            self.object = form.save(commit=False)
            test_case = test_case_form.save(commit=False)

            self.object.test_case = test_case
            self.object.save()  # save problem object
            form.save_m2m()  # save many-to-many fields

            test_case.problem = self.object
            test_case.save()  # save test object

            judge_problem_solution.delay(self.object.pk)

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


class AutocompleteTagsView(View):
    def get(self, request):
        prefix = request.GET['search']
        tags = Tag.objects.filter(name__startswith=prefix)

        response = []
        for tag in tags:
            response.append({'text': tag.name, 'value': tag.pk})

        return JsonResponse(response, safe=False)
