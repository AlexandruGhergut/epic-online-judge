from django.conf.urls import url

from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^submission/$', views.ListSubmissionView.as_view(),
        name='list_submissions'),
    url(r'^submission/(?P<pk>[0-9]+)/$', views.SourceView.as_view(),
        name='view_source'),
    url(r'^submission/(?P<pk>[0-9]+)/submit/$',
        views.SourceSubmitView.as_view(), name='submit_source'),
    url(r'^submission/(?P<pk>[0-9]+)/contest/(?P<contest_pk>[0-9]+)/submit/$',
        views.ContestSourceSubmitView.as_view(), name='submit_contest_source'),
    url(r'^submission/status/$', views.GetSubmissionStatusView.as_view()),
]
