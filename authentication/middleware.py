from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect


class SetUsernameRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            redirect_url = reverse('authentication:set_username',
                                   kwargs={'pk': user.pk})
            if (request.path != redirect_url and user.username_set is False):
                request.session['set_username'] = True
                return HttpResponseRedirect(redirect_url)
