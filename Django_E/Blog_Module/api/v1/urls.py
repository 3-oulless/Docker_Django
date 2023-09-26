from .views import (
    PostModelViewSet,
    CategoryModelViewSet,
)
from rest_framework.routers import (
    DefaultRouter,
)


app_name = "api_v1"

router = DefaultRouter()
router.register(
    "post",
    PostModelViewSet,
    basename="post",
)
router.register(
    "category",
    CategoryModelViewSet,
    basename="category",
)

urlpatterns = []

urlpatterns += router.urls


"""
urlpatterns = [
    function base
    path('',product_function_api,name='test_function'),
    path('<int:id>/',product_detail_function_api,name='post_function'),

    #class Base_APIView
    path('api_view/',ProductList_ApiView.as_view(),name='api_view_list'),
    path('api_view/<int:pk>',ProductDetail_ApiView.as_view(),name='api_view_detail'),

    #class base generiv
    path('post/',PostListSerializer.as_view(),name='PostListSerializer'),
    path('post/<int:id>/',PostDetailSerializer.as_view(),name='PostDetailSerializer'),

    class base viewset
    path('view_set/',PostViewSet.as_view({'get':'list','post':'create'}),name='api_viewset_get_post'),
    path('view_set/<pk>/',PostViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}),name='api_viewset_detail'),

]
"""
