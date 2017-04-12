from django.conf.urls import url

from . import views

app_name = 'authentication'
urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^confirm_email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ConfirmEmailView.as_view(), name='activate_account'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout')
]
