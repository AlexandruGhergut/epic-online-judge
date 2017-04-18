from django.views.generic.edit import FormView
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout, get_user_model

from oauth2client import client, crypt

from .forms import RegisterForm, LoginForm
from .tokens import account_activation_token
from common import utils, strings

User = get_user_model()


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
        messages.info(self.request, strings.REGISTRATION_EMAIL_SENT)
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
                    messages.success(request,
                                     strings.REGISTRATION_EMAIL_CONFIRMED)
                    return redirect('core:index')

        messages.error(request,
                       strings.REGISTRATION_CONFIRMATION_TOKEN_INVALID)
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


class GoogleLoginView(View):
    def post(self, request):
        import pdb; pdb.set_trace()
        token = request.POST.get('idtoken', '')
        CLIENT_ID = '366014831250-pja5mp5spctso4ij1jidho54ujqcq2h4.apps.googleusercontent.com'
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
        except crypt.AppIdentityError:
            pass
        userid = idinfo['sub']

        return redirect('core:index')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:index')
