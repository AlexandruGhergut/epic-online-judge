from django.conf.urls import url

from . import views

app_name = 'contest'
urlpatterns = [
    url(r'^$', views.ListContestsView.as_view(), name='list_contests'),
    url(r'^create$', views.CreateContestView.as_view(), name='create_contest'),
]
