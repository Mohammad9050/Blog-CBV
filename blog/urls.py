from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from . import views

app_name = "blog"
urlpatterns = [
    # path('', TemplateView.as_view(template_name = 'index.html', extra_context={'name':'ali'}))
    path("", views.IndexView.as_view(), name="index"),
    # path('redirect', RedirectView.as_view(url='https://www.google.com'), name='redirect')
    path("redirect", RedirectView.as_view(pattern_name="blog:index"), name="redirect"),
    path("posts/", views.PostList.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostDetail.as_view(), name="detail"),
    # both of form and create work same
    path("posts/form/", views.PostForm.as_view(), name="form"),
    path("posts/create/", views.PostCreate.as_view(), name="create"),
    path("posts/<int:pk>/update/", views.PostUpdate.as_view(), name="update"),
    path("posts/<int:pk>/delete/", views.PostDelete.as_view(), name="delete"),
    path("api/v1/", include("blog.api.v1.urls")),
]
