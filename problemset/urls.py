from django.conf.urls import url

from . import views

app_name = 'problemset'
urlpatterns = [
    url(r'^problem/create/$', views.CreateProblemView.as_view(),
        name='create_problem'),
    url(r'^$', views.ListProblemsView.as_view(), name='list_problems'),
    url(r'^problem/(?P<pk>[0-9]+)/$', views.DetailProblemView.as_view(),
        name='view_problem'),
    url(r'^problem/(?P<pk>[0-9]+)/edit/$', views.UpdateProblemView.as_view(),
        name='edit_problem'),
    url(r'^problem/tag/$', views.AutocompleteTagsView.as_view()),
    url(r'^problem/autocomplete/$', views.AutocompleteProblemsView.as_view(),
        name='autocomplete_problems'),
]
