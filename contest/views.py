from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from problemset.forms import TestCaseForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from common import strings
from .models import Contest
from .forms import ContestForm, ContestProblemForm
from core.forms import SubmissionForm
from core.models import Submission
from problemset.models import Problem
from problemset.tasks import judge_problem_solution


class ListContestsView(View):
    def get(self, request):
        time = timezone.now()
        active_contests = Contest.objects\
            .filter(start_datetime__lte=time).filter(end_datetime__gte=time)
        upcoming_contests = Contest.objects\
            .filter(start_datetime__gt=time)
        past_contests = Contest.objects\
            .filter(end_datetime__lt=time)

        context = {'upcoming_contests': upcoming_contests,
                   'past_contests': past_contests,
                   'active_contests': active_contests,
                   'current_datetime': time}
        return render(request, 'contest/list_contests.html', context)


class CreateContestView(LoginRequiredMixin, CreateView):
    form_class = ContestForm
    template_name = "contest/create_contest.html"
    success_url = reverse_lazy('contest:list_contests')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateContestView, self).form_valid(form)


class DetailContestView(View):
    def get(self, request, pk):
        contest = get_object_or_404(Contest, pk=pk)
        context = {'object': contest}
        return render(request, 'contest/view_contest.html', context)


class CreateContestProblemView(LoginRequiredMixin, PermissionRequiredMixin,
                               CreateView):
    form_class = ContestProblemForm
    template_name = "contest/create_contest_problem.html"
    permission_required = 'problemset.can_add_problem'

    def get(self, request, pk, *args, **kwargs):
        contest = get_object_or_404(Contest, pk=pk)
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        test_case_form = TestCaseForm()

        return self.render_to_response(
            self.get_context_data(form=form, contest=contest,
                                  test_case_form=test_case_form)
        )

    def post(self, request, pk, *args, **kwargs):
        contest = get_object_or_404(Contest, pk=pk)
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        test_case_form = TestCaseForm(self.request.POST,
                                      self.request.FILES)
        form.instance.publish_datetime = contest.end_datetime
        print(form.instance.publish_datetime)
        if (form.is_valid() and test_case_form.is_valid()):
            form.instance.user = self.request.user

            self.object = form.save(commit=False)
            test_case = test_case_form.save(commit=False)

            self.object.test_case = test_case
            self.object.save()  # save problem object
            form.save_m2m()  # save many-to-many fields

            test_case.problem = self.object
            test_case.save()  # save test object

            contest.problems.add(self.object)
            judge_problem_solution.delay(self.object.pk)

            return HttpResponseRedirect(reverse('contest:view_contest',
                                                kwargs={'pk': contest.pk}))
        print(form._errors)
        return self.render_to_response(
            self.get_context_data(form=form, contest=contest,
                                  test_case_form=test_case_form)
        )

    def handle_no_permission(self):
        messages.error(self.request, strings.PERMISSIONS_MISSING)
        return super(CreateContestProblemView, self).handle_no_permission()


class DetailContestProblemView(DetailView):
    model = Problem
    template_name = 'contest/view_contest_problem.html'

    def get_context_data(self, **kwargs):
        context = super(DetailContestProblemView, self)\
            .get_context_data(**kwargs)
        submission_form = SubmissionForm()
        context['submission_form'] = submission_form
        contest_pk = self.kwargs['contest_pk']
        contest = get_object_or_404(Contest, pk=contest_pk)
        if timezone.now() <= contest.end_datetime:
            context['is_contest_submission'] = True
        else:
            context['is_contest_submission'] = False
        context['contest'] = contest
        return context

# class StandingsView(View):
#     def get(self, request, pk):
#         contest = get_object_or_404(Contest, pk=pk)
#         participants = Submission.objects.filter(contest=contest)\
#             .distinct('user')
#         for participant in participants:
