from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .forms import PostForm


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "blog/create_post.html"
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreatePostView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
