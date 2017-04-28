from datetime import datetime
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProblemForm
from .models import Problem


class CreateProblemView(LoginRequiredMixin, CreateView):
    form_class = ProblemForm
    template_name = "common/content_center_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateProblemView, self).form_valid(form)


class ListProblemsView(ListView):
    template_name = 'problemset/list_problems.html'
    queryset = Problem.objects.filter(publish_datetime__lte=datetime.now())


class DetailProblemView(DetailView):
    model = Problem
    template_name = 'problemset/view_problem.html'
