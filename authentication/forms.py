from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML, ButtonHolder

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = \
        forms.EmailField(max_length=256,
                         help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username/Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('authentication:login')
        self.helper.layout = Layout(
            Div(
                Field(
                    'username_or_email',
                    css_class='form-control',
                    ),
                css_class='form-group'
                ),
            Div(
                HTML('<a class="pull-right" href="#">Forgot password?</a>'),
                Field(
                    'password',
                    css_class='form-control'
                    ),
                css_class='form-group'
            ),
            Div(
                HTML('<a href="{% url \'authentication:register\' %}">Don\'t '
                     'have an account? Create one</a>'),
                css_class='form-group'
                ),
            Div(
                ButtonHolder(
                    Submit('submit', 'Submit'),
                ),
                css_class='form-group',
                ),
        )

    def clean(self, *args, **kwargs):
        username_or_email = self.cleaned_data.get("username_or_email")
        password = self.cleaned_data.get("password")

        user = User.objects.filter(Q(username=username_or_email) |
                                   Q(email=username_or_email)).first()

        if not user:
            raise forms.ValidationError('No account with that '
                                        'username/email exists')

        if not user.check_password(password):
            raise forms.ValidationError('Wrong password')

        if user.profile.email_confirmed is False:
            raise forms.ValidationError('Email is not confirmed')

        return super(LoginForm, self).clean(*args, **kwargs)
