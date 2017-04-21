from django.views.generic.edit import FormView, UpdateView
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import resolve
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.db.models import Q
from django.conf import settings
from django.http.response import HttpResponseRedirect
from .forms import (RegisterForm, LoginForm, RequestPasswordResetForm,
                    ChangePasswordForm, ChangeUsernameForm)
from .tokens import account_activation_token, password_reset_token
from common import utils, strings

User = get_user_model()


class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:index')
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        site = get_current_site(self.request)
        subject = 'Activate account'
        message = \
            render_to_string('authentication/confirm_email_message.html', {
                'username': self.request.user.username,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        user.email_user(subject, message)
        messages.info(self.request, strings.REGISTRATION_EMAIL_SENT)
        return redirect('authentication:login')


class ConfirmEmailView(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:index')
        return super(ConfirmEmailView, self).dispatch(*args, **kwargs)

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and \
                account_activation_token.check_token(user, token):
                    user.is_active = True
                    user.profile.email_confirmed = True
                    user.save()
                    login(request, user)
                    messages.success(request,
                                     strings.REGISTRATION_EMAIL_CONFIRMED)
                    return redirect('core:index')

        messages.error(request,
                       strings.REGISTRATION_CONFIRMATION_TOKEN_INVALID)
        return redirect('authentication:register')


class LoginView(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:index')
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get(self, request):
        form = LoginForm()
        context = {'form': form, 'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID}
        return render(request, 'authentication/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('core:index')

        utils.display_validation_errors(request, form)
        return redirect('authentication:login')


class GoogleLoginView(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:index')
        return super(GoogleLoginView, self).dispatch(*args, **kwargs)

    def post(self, request):
        token = request.POST.get('idtoken', '')
        user = authenticate(token=token)
        if user is not None:
            login(request, user)
            return redirect('core:index')

        messages.error(request, strings.AUTH_TOKEN_INVALID)
        return redirect('authentication:login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:index')


# This view is used to file a request for password change
class RequestPasswordResetView(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:index')
        return super(RequestPasswordResetView, self).dispatch(*args, **kwargs)

    def get(self, request):
        form = RequestPasswordResetForm()
        return render(request, 'authentication/request_password_reset.html',
                      {'form': form})

    def post(self, request):
        form = RequestPasswordResetForm(request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            user = User.objects.filter(Q(username=username_or_email) |
                                       Q(email=username_or_email)).first()

            site = get_current_site(self.request)
            subject = 'Reset your password'
            message_template = 'authentication/reset_password_message.html'
            message = \
                render_to_string(message_template, {
                    'username': request.user.username,
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': password_reset_token.make_token(user),
                })
            user.email_user(subject, message)
            messages.success(request, strings.PASSWORD_RESET_EMAIL_SENT)
            return redirect('authentication:login')

        utils.display_validation_errors(request, form)
        return redirect('authentication:login')


class ChangePasswordView(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:index')
        return super(ChangePasswordView, self).dispatch(*args, **kwargs)

    def __get_user_by_token(self, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        return user

    def get(self, request, uidb64, token):
        template_name = 'authentication/request_password_reset.html'

        user = self.__get_user_by_token(uidb64, token)
        if user is not None and password_reset_token.check_token(user, token):
            form = ChangePasswordForm(user, uidb64=uidb64, token=token)
            return render(request, template_name, {'form': form})

        messages.error(request, strings.PASSWORD_RESET_TOKEN_INVALID)
        return redirect('authentication:login')

    def post(self, request, uidb64, token):
        user = self.__get_user_by_token(uidb64, token)
        if user is not None and password_reset_token.check_token(user, token):
            form = ChangePasswordForm(user, request.POST, uidb64=uidb64,
                                      token=token)
            if form.is_valid():
                form.save()
                messages.success(request, strings.PASSWORD_RESET_SUCCESSFULL)
                return redirect('authentication:login')
            else:
                utils.display_validation_errors(request, form)
                return redirect('authentication:change_password',
                                uidb64=uidb64, token=token)
        else:
            messages.error(request, strings.PASSWORD_RESET_TOKEN_INVALID)
            return redirect('authentication:login')


class ChangeUsernameView(LoginRequiredMixin, UpdateView):
    template_name = 'authentication/change_username.html'
    form_class = ChangeUsernameForm
    model = User

    def dispatch(self, *args, **kwargs):
        if 'set_username' not in self.request.session:
            return redirect('core:index')
        return super(ChangeUsernameView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(ChangeUsernameView, self).get_initial()
        initial['username'] = ''
        return initial

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.username_set = True
        del self.request.session['set_username']
        return super(ChangeUsernameView, self).form_valid(form)
