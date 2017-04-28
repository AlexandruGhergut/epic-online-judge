from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Submit, Layout, Field, Div,
                                 ButtonHolder)
from .models import Problem


class ProblemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('problemset:create_problem')
        self.helper.layout = Layout(
            Div(
                Field(
                    'title',
                    css_class='form-control',
                    ),
                Field(
                    'statement',
                    css_class='form-control',
                    ),
                Field(
                    'publish_datetime',
                    css_class='form-control',
                    ),
                css_class='form-group'
                ),
            Div(
                ButtonHolder(
                    Submit('submit', 'Submit'),
                ),
                css_class='form-group',
                ),
        )

    class Meta:
        model = Problem
        exclude = ['user']
