from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Field, Div, ButtonHolder, Submit,
                                 HTML)
from problemset.forms import ProblemForm
from problemset.models import Problem
from .models import Contest


class ContestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('contest:create_contest')
        self.helper.layout = Layout(
            Div(
                Field(
                    'title',
                    css_class='form-control',
                    ),
                Field(
                    'start_datetime',
                    css_class='form-control datetime-field',
                    ),
                Field(
                    'end_datetime',
                    css_class='form-control datetime-field',
                ),
                HTML(
                    '<p><strong>Note that after submitting your contest, you must add problems to it</strong></p>',
                ),
                ButtonHolder(
                    Submit('submit', 'Submit'),
                ),
                css_class='form-group'
                ),
        )

    class Meta:
        model = Contest
        exclude = ['author', 'problems']


class ContestProblemForm(ProblemForm):
    def __init__(self, *args, **kwargs):
        super(ContestProblemForm, self).__init__(*args, **kwargs)
        self.fields.pop('publish_datetime')
