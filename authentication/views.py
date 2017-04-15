from django.views.generic.edit import FormView
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout
from .forms import RegisterForm, LoginForm
from .tokens import account_activation_token
from common import utils


class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        site = get_current_site(self.request)
        subject = 'Activate account'
        message = \
            render_to_string('authentication/confirm_email_message.html', {
                'username': user.username,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        user.email_user(subject, message)

        return redirect('authentication:login')


class ConfirmEmailView(View):
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
                    messages.success(request, 'Email confirmed')
                    return redirect('authentication:index')

        messages.error(request, 'Invalid token')
        return redirect('authentication:register')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('core:index')

        utils.display_validation_errors(request, form)
        return redirect('authentication:login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:index')
