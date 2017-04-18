from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
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
    username = forms.CharField(label="Username")
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
                    'username',
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
                HTML('<a href="{% url \'authentication:register\' %}">Don\'t have an account? Create one</a>'),
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
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = User.objects.filter(username=username).first()

        if not user:
            raise forms.ValidationError("No account with that username exists")

        if not user.check_password(password):
            raise forms.ValidationError("Wrong password")

        if user.profile.email_confirmed is False:
            raise forms.ValidationError("Email is not confirmed")

        return super(LoginForm, self).clean(*args, **kwargs)
