from django.conf.urls import url

from . import views


app_name = 'blog'
urlpatterns = [
    url(r'^$', views.CreatePostView.as_view(), name='create_post'),
]
