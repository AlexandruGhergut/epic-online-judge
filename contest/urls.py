from django.conf.urls import url

from . import views

app_name = 'contest'
urlpatterns = [
    url(r'^$', views.ListContestsView.as_view(), name='list_contests'),
    url(r'^create$', views.CreateContestView.as_view(), name='create_contest'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailContestView.as_view(),
        name='view_contest'),
    url(r'^(?P<pk>[0-9]+)/create_problem/$',
        views.CreateContestProblemView.as_view(), name='create_problem'),
    url(r'^(?P<contest_pk>[0-9]+)/problem/(?P<pk>[0-9]+)/$',
        views.DetailContestProblemView.as_view(), name='view_problem')
]
