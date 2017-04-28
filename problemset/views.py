from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from problemset.forms import ProblemForm


class CreateProblemView(LoginRequiredMixin, CreateView):
    form_class = ProblemForm
    template_name = "problemset/create_problem.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateProblemView, self).form_valid(form)
