from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Field, Div, ButtonHolder, Submit)
from .models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        self.user = request.user
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                Field('title',
                      css_class='form-control'),
                Field('content'),
                css_class='form-group ',
                ),
        )
        if request.user.has_perm('can_post_on_homepage'):
            self.helper.layout.append((Field('on_homepage')))
        self.helper.layout.append(
            ButtonHolder(
                Submit('submit', 'Submit'),
            )
        )

    class Meta:
        model = Post
        fields = ('title', 'content', 'on_homepage')
