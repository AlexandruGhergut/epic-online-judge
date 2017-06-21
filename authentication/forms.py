from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.forms import SetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Submit, Layout, Field, Div, HTML,
                                 ButtonHolder, Fieldset)
from timezone_field import TimeZoneFormField

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = \
        forms.EmailField(max_length=256,
                         help_text='Required. Enter a valid email address.')
    timezone = TimeZoneFormField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('authentication:register')
        self.helper.layout = Layout(
            Div(
                Field(
                    'username',
                    css_class='form-control',
                    ),
                Field(
                    'email',
                    css_class='form-control',
                    ),
                Field(
                    'password1',
                    css_class='form-control',
                    ),
                Field(
                    'password2',
                    css_class='form-control',
                    ),
                Field(
                    'timezone',
                    css_class='form-control',
                    ),
                css_class='form-group',
                ),
            Div(
                ButtonHolder(
                    Submit('submit', 'Submit'),
                ),
            ),
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'timezone')


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username/Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
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
                HTML('<a class="pull-right" '
                     'href="{% url \'authentication:reset_password\' %}">'
                     'Forgot password?</a>'),
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

        if user.is_active is False:
            raise forms.ValidationError('Account is not active')

        return super(LoginForm, self).clean(*args, **kwargs)


class RequestPasswordResetForm(forms.Form):
    username_or_email = forms.CharField(label='Username/Email')

    def __init__(self, *args, **kwargs):
        super(RequestPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('authentication:reset_password')
        self.helper.layout = Layout(
            Fieldset('Password recovery',
                     Div(
                        Field(
                            'username_or_email',
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
                )

    def clean(self, *args, **kwargs):
        username_or_email = self.cleaned_data.get('username_or_email')

        user = User.objects.filter(Q(username=username_or_email) |
                                   Q(email=username_or_email)).first()

        if not user:
            raise forms.ValidationError('No account with that '
                                        'username/email exists')

        if user.is_active is False:
            raise forms.Validationerror('Accout is not active')

        return super(RequestPasswordResetForm, self).clean(*args, **kwargs)


class ChangePasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        data = {}
        if 'uidb64' in kwargs:
            data['uidb64'] = kwargs.pop('uidb64')
        if 'token' in kwargs:
            data['token'] = kwargs.pop('token')

        super(ChangePasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].help_text = ''
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('authentication:change_password',
                                          kwargs=data)
        self.helper.layout = Layout(
            Div(
                Field(
                    'new_password1',
                    css_class='form-control',
                    ),
                Field(
                    'new_password2',
                    css_class='form-control'
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


class ChangeUsernameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            Div(
                Field(
                    'username',
                    default='',
                    css_class='form-control',
                    ),
                ButtonHolder(
                    Submit('submit', 'Submit'),
                ),
                css_class='form-group',
                )
            )

    class Meta:
        model = User
        fields = ('username',)
