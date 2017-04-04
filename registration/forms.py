from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = \
        forms.EmailField(max_length=256,
                         help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('email_confirmed',)
