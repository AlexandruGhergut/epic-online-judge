from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Submit, Layout, Field, Div,
                                 ButtonHolder, HTML)
from django.forms.models import formset_factory
from .models import Problem, TestCase, Submission


class ProblemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
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
                    css_class='form-control datetime-field',
                    ),
                Field(
                    'sample_input',
                    css_class='form-control',
                    ),
                Field(
                    'sample_output',
                    css_class='form-control',
                    ),
                Field(
                    'solution_source_file',
                ),
                css_class='form-group'
                ),
        )

    class Meta:
        model = Problem
        exclude = ['user']


class TestCaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestCaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('input_data_file'),
        )

    class Meta:
        model = TestCase
        exclude = ['problem']


class SubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Div(
                Field('source_file'),
                ButtonHolder(
                    Submit('submit', 'Submit'),
                ),
                css_class='form-group',
                ),
        )

    class Meta:
        model = Submission
        fields = ('source_file',)


TestCaseFormSet = formset_factory(TestCaseForm)
