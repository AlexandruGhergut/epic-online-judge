from django.views.generic.edit import FormView
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import UserCreationForm
from .tokens import account_activation_token


class IndexView(FormView):
    template_name = 'registration/index.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        site = get_current_site(self.request)
        subject = 'Activate account'
        message = \
            render_to_string('registration/account_activation_email.html', {
                'username': user.username,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        user.email_user(subject, message)

        return redirect('register')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and \
                account_activation_token.check_token(user, token):
                    user.profile.email_confirmed = True
                    user.save()
                    login(request, user)
                    return redirect('register')
        return redirect('register')
