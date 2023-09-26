from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework import (
    viewsets,
)
from .serializers import (
    PostSerializer,
    CategorySerializer,
)
from Blog_Module.models import (
    Post,
    Category,
)
from .permisions import (
    IsOwnerOrReadOnly,
)
from .paginations import (
    DefaultPagination,
)

# filters
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_date")
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    serializer_class = PostSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_fields = {
        "author": ["exact"],
        "category": [
            "exact",
            "in",
        ],
        "status": ["exact"],
    }
    search_fields = [
        "=title",
        "=content",
    ]
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    serializer_class = CategorySerializer
