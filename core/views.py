from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'core/index.html', {'user': request.user})
