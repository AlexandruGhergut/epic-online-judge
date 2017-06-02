from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Field, Div, ButtonHolder, Submit)
from .models import Submission


class SubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('source_file'),
                Field('language'),
                ButtonHolder(
                    Submit('submit', 'Submit'),
                ),
                css_class='form-group',
                ),
        )

    class Meta:
        model = Submission
        fields = ('source_file', 'language',)
