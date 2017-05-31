import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated():
            tzname = request.user.timezone.zone
        else:
            tzname = 'Europe/London'

        timezone.activate(pytz.timezone(tzname))
