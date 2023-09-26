
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework import viewsets
from Blog_Module.models import Post
from .serializers import PostSerializer, CategorySerializer
from Blog_Module.models import Post, Category
from .permisions import IsOwnerOrReadOnly
from .paginations import DefaultPagination

# filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


"""
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def product_function_api(request):
    if request.method == "GET":
        post = Post.objects.all()
        srz = PostSerializer(post,many=True)
        return Response(srz.data)
    elif request.method == "POST":
        srz = PostSerializer(data=request.data)
        srz.is_valid(raise_exception=True)
        srz.save()
        return Response(srz.data)


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def product_detail_function_api(request,id):
    
    try:
        post = Post.objects.get(pk=id,status=True)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        srz = PostSerializer(post)
        return Response(srz.data)

    elif request.method == 'PUT':
        srz = PostSerializer(post,data=request.data)
        srz.is_valid(raise_exception=True)
        srz.save()
        return Response(srz.data)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList_ApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    def get(self,request,format=None):
        post = Post.objects.all()
        srz = PostSerializer(post,many=True)
        return Response(srz.data,status=status.HTTP_200_OK)
    
    def post(self,request,format=None):
        srz = PostSerializer(data=request.data)
        srz.is_valid(raise_exception=True)
        srz.save()
        return Response(srz.data,status=status.HTTP_201_CREATED)

class ProductDetail_ApiView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk,status=True)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get(self,request,pk,format=None):
        post = self.get_object(pk)
        srz = self.serializer_class(post)
        return Response(srz.data)
    
    def put(self,request,pk,format=None):
        post = self.get_object(pk)
        srz = self.serializer_class(post,data=request.data)
        srz.is_valid(raise_exception=True)
        srz.save()
        return Response(srz.data,status=status.HTTP_200_OK)
    
    def delete(self,request,pk,format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PostListSerializer(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostDetailSerializer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class PostViewSet(viewsets.ViewSet):
    
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def list(self,request):
        post = Post.objects.all()
        srz = self.serializer_class(post,many=True)
        return Response(srz.data)
    
    def create(self,request):
        srz = self.serializer_class(data=request.data)
        srz.is_valid(raise_exception=True)
        srz.save()
        return Response(srz.data,status=status.HTTP_201_CREATED)
    
    def retrieve(self,request,pk=None):
        post = get_object_or_404(Post,pk=pk)
        srz = PostSerializer(post)
        return Response(srz.data)
    
    def update(self, request, pk=None):
        post = get_object_or_404(Post,pk=pk)
        srz = self.serializer_class(post,data=request.data)
        srz.is_valid(raise_exception=True) 
        srz.save()
        return Response(srz.data,status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        post = get_object_or_404(Post,pk=pk)
        srz = self.serializer_class(post,data=request.data)
        srz.is_valid(raise_exception=True)
        srz.save()
        return Response(srz.data,status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        post = get_object_or_404(Post,pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_date")
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "author": ["exact"],
        "category": ["exact", "in"],
        "status": ["exact"],
    }
    search_fields = ["=title", "=content"]
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CategorySerializer
