from datetime import datetime
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import ProblemForm, TestCaseFormSet
from .models import Problem


class CreateProblemView(LoginRequiredMixin, CreateView):
    form_class = ProblemForm
    template_name = "problemset/create_problem.html"
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        test_case_formset = TestCaseFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  test_case_formset=test_case_formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        test_case_formset = TestCaseFormSet(self.request.POST,
                                            self.request.FILES)
        if (form.is_valid() and test_case_formset.is_valid()):
            return self.form_valid(form, test_case_formset)
        else:
            return self.form_invalid(form, test_case_formset)

    def form_valid(self, form, test_case_formset):
        form.instance.user = self.request.user
        self.object = form.save()
        for test_form in test_case_formset.forms:
            test_form.instance.problem = self.object
            test_form.instance.save()
        return HttpResponseRedirect(self.get_success_url())

        return super(CreateProblemView, self).form_valid(form)

    def form_invalid(self, form, test_case_formset):
        return self.render_to_context(
            self.get_context_data(form=form,
                                  test_case_formset=test_case_formset)
        )


class ListProblemsView(ListView):
    template_name = 'problemset/list_problems.html'
    queryset = Problem.objects.filter(publish_datetime__lte=datetime.now())


class DetailProblemView(DetailView):
    model = Problem
    template_name = 'problemset/view_problem.html'
