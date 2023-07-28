from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter

routers = DefaultRouter()
routers.register("posts", views.PostModelViewSet, basename="post")
routers.register("category", views.CategoryModelViewSet, basename="category")


app_name = "api"

urlpatterns = routers.urls

# urlpatterns = [
#     # path('posts/<int:id>/', views.api_detail, name='detail'),
#     # path('posts/', views.api_list, name='list')
#     path('posts/', views.PostList.as_view(), name='list'),

#     path('posts/<int:pk>/', views.PostDetail.as_view(), name='detail')
# ]
