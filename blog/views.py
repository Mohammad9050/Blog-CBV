from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from blog.forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import Profile

# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"
    #permission_required = "blog.view_post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "mamad"
        context["posts"] = Post.objects.all()
        return context


class PostList(ListView):
    model = Post
    # change name of context
    context_object_name = "posts"
    # overwrite query
    # queryset = Post.objects.all()
    paginate_by = 2
    ordering = "-id"
    # for custom query
    # def get_queryset(self):
    # posts = Post.objects.filter(status=False)
    # return posts


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post


class PostForm(FormView):
    template_name = "content.html"
    form_class = PostForm
    success_url = "/posts/"

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)


class PostCreate(CreateView):
    model = Post
    fields = ["title", "content", "status"]
    success_url = "/posts/"

    def form_valid(self, form):  # for choose user automatic
        user = Profile.objects.get(user=self.request.user)
        form.instance.author = user
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ["title", "content", "status"]
    success_url = "/posts/"


class PostDelete(DeleteView):
    model = Post
    success_url = "/posts/"
