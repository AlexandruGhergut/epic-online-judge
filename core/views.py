from django.shortcuts import render
from django.views import View
from django.conf import settings


class IndexView(View):
    def get(self, request):
        return render(request, 'core/index.html',
                      {'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID})
