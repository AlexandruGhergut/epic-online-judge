from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.shortcuts import redirect
from core.forms import SubmissionForm
from common import strings
from .forms import (ProblemForm, TestCaseForm, UpdateProblemForm,
                    UpdateTestCaseForm)
from .models import Problem, Tag
from .tasks import judge_problem_solution


class CreateProblemView(LoginRequiredMixin, PermissionRequiredMixin,
                        CreateView):
    form_class = ProblemForm
    template_name = "problemset/create_problem.html"
    permission_required = 'problemset.can_add_problem'

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

    def handle_no_permission(self):
        messages.error(self.request, strings.PERMISSIONS_MISSING)
        return super(CreateProblemView, self).handle_no_permission()


class UpdateProblemView(LoginRequiredMixin, UpdateView):
    model = Problem
    form_class = UpdateProblemForm
    template_name = 'problemset/update_problem.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.user:
            messages.error(self.request, strings.PERMISSIONS_MISSING)
            return redirect('core:index')

        form_class = self.get_form_class()
        form = form_class(instance=self.object)
        test_case_form = UpdateTestCaseForm()

        return self.render_to_response(
            self.get_context_data(form=form, object=form.instance,
                                  test_case_form=test_case_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.user:
            messages.error(self.request, strings.PERMISSIONS_MISSING)
            return redirect('core:index')

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        test_case_form = UpdateTestCaseForm(self.request.POST,
                                            self.request.FILES)

        if (form.is_valid() and test_case_form.is_valid()):
            form.instance.user = self.request.user

            new_object = form.save(commit=False)
            new_test_case = test_case_form.save(commit=False)

            self.object.user = new_object.user
            self.object.title = new_object.title
            self.object.statemenet = new_object.statement
            self.object.input_description = new_object.input_description
            self.object.output_description = new_object.output_description
            self.object.publish_datetime = new_object.publish_datetime
            self.object.sample_input = new_object.sample_input
            self.object.sample_output = new_object.sample_output
            if new_object.solution_source_file.name:
                self.object.solution_source_file =\
                    new_object.solution_source_file

            if new_test_case.input_data_file.name:
                prev_test_case = self.object.testcase
                self.object.testcase = new_test_case
                prev_test_case.delete()

            self.object.save()  # save problem object
            form.save_m2m()  # save many-to-many fields

            if new_test_case.input_data_file.name:
                new_test_case.problem = self.object
                new_test_case.save()  # save test object

            judge_problem_solution.delay(self.object.pk)

            return HttpResponseRedirect(self.get_success_url())

        return self.render_to_response(
            self.get_context_data(form=form, object=self.object,
                                  test_case_form=test_case_form)
        )


class ListProblemsView(ListView):
    model = Problem
    template_name = 'problemset/list_problems.html'

    def get_queryset(self):
        fields = ('tags',)
        query_dict = {}
        for field in fields:
            value = self.request.GET.get(field)
            if value:
                query_dict[field] = value

        return Problem.objects.filter(publish_datetime__lte=timezone.now())\
            .filter(**query_dict).order_by('-publish_datetime')


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


class AutocompleteProblemsView(View):
    def get(self, request):
        prefix = request.GET['search']
        problems = Problem.objects.filter(title__startswith=prefix)

        response = []
        for problem in problems:
            response.append({'text': problem.title, 'value': problem.pk})

        return JsonResponse(response, safe=False)
