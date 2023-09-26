from django.urls import path, include
from .views import PostList, DetailPost, CreatePost, UpdatePost, DeletePost,IndexView


app_name = "post"

urlpatterns = [
    path('index/',IndexView.as_view(),name='index'),
    # MVT
    path("", PostList.as_view(), name="post-list"),
    path("<pk>", DetailPost.as_view(), name="post-detail"),
    path("create/", CreatePost.as_view(), name="post-create"),
    path("update/<pk>/", UpdatePost.as_view(), name="post-update"),
    path("delete/<pk>/", DeletePost.as_view(), name="post-delete"),
    # END MVT
    # SERIALIZERS
    path("api/v1/", include("Blog_Module.api.v1.urls", namespace="api_v1")),
]
