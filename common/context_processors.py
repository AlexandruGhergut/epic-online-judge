from django.conf import settings


def init(request):
    return {'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID}
