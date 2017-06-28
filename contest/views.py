from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic.edit import CreateView
from .models import Contest
from .forms import ContestForm


class ListContestsView(View):
    def get(self, request):
        upcoming_contests = Contest.objects\
            .filter(start_datetime__gt=timezone.now())
        past_contests = Contest.objects\
            .filter(start_datetime__lt=timezone.now())

        context = {'upcoming_contests': upcoming_contests,
                   'past_contests': past_contests}
        return render(request, 'contest/list_contests.html', context)


class CreateContestView(LoginRequiredMixin, CreateView):
    form_class = ContestForm
    template_name = "contest/create_contest.html"
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateContestView, self).form_valid(form)
