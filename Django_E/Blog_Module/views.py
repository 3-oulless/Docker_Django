from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import Post
from .forms import CreateOrUpdatePostModel
from django.contrib.auth.mixins import LoginRequiredMixin



# MVT


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['name'] = 'ali'
        return context

class PostList(LoginRequiredMixin, ListView):
    login_url = "/account/login/"
    model = Post
    template_name = "Post/PostList.html"
    context_object_name = "Posts"
    ordering = "-id"


class DetailPost(LoginRequiredMixin, DetailView):
    login_url = "/account/login/"
    model = Post
    template_name = "Post/PostDetail.html"
    context_object_name = "post"


class CreatePost(LoginRequiredMixin, CreateView):
    login_url = "/account/login/"
    model = Post
    template_name = "Post/PostCreate.html"
    form_class = CreateOrUpdatePostModel
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UpdateView):
    login_url = "/account/login/"
    model = Post
    template_name = "Post/PostCreate.html"
    form_class = CreateOrUpdatePostModel
    success_url = "/"


class DeletePost(LoginRequiredMixin, DeleteView):
    login_url = "/account/login/"
    model = Post
    success_url = "/"
    template_name = "Post/PostDelete.html"


# END MVT
