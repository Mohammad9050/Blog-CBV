from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from blog.models import Post, Category
from .serializers import PostSer, CategorySer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import CustomPagination


## function based view
"""
@api_view(['GET','PUT', 'DELETE'])
#@permission_classes([IsAuthenticatedOrReadOnly])
def api_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'GET':

        ser = PostSer(post)
        return Response(ser.data)
    elif request.method == 'PUT':
        ser = PostSer(post, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
    else:
        post.delete()
        return Response({'detail':'item deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
#@permission_classes([IsAuthenticated])
def api_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        ser = PostSer(posts, many=True)
        return Response(ser.data)
    else:
        ser = PostSer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
"""
##class based view
"""
class PostList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSer
    def get(self, request):
        posts = Post.objects.all()
        ser = PostSer(posts, many=True)
        return Response(ser.data)
    def post(sel, request):
        ser = PostSer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

        
class PostDetail(APIView):
    serializer_class = PostSer

    def get(self, request, id):
        post = get_object_or_404(Post, pk=id)
        ser = self.serializer_class(post)
        return Response(ser.data)
    
    def put(self, request, id):
        post = get_object_or_404(Post, pk=id)
        ser = self.serializer_class(post, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
    
    def delete(self, request, id):
        post = get_object_or_404(Post, pk=id)
        post.delete()
        return Response({'detail':'item deleted'}, status=status.HTTP_204_NO_CONTENT)
"""
## Generic API view
"""
class PostList(ListCreateAPIView):
    serializer_class = PostSer
    queryset = Post.objects.all()


class PostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSer
    queryset = Post.objects.all()


"""
## ViewSet
"""
class PostViewSet(viewsets.ViewSet):
    serializer_class = PostSer
    queryset = Post.objects.all()

    def list(self, request):
        ser = self.serializer_class(self.queryset, many=True)
        return Response(ser.data)
    
    def retrieve(self, request, pk=None):
        obj = get_object_or_404(self.queryset, pk=pk)
        ser = self.serializer_class(obj)
        return Response(ser.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    def create(self, request):
        pass
"""
## Model ViewSet


class PostModelViewSet(viewsets.ModelViewSet):
   # permission_classes = [IsAuthenticated]
    serializer_class = PostSer
    queryset = Post.objects.all()
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]  # filter result

    filterset_fields = {"category": ["exact", "in"], "author": []}  # fields for filter
    search_fields = ["title", "content"]  # fields for search
    ordering_fields = ["published_date"]  # fields for order

    # extra url and activity
    @action(detail=False, methods=["get"])
    def get_ok(self, request):
        return Response({"detail": "ok"})


class CategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySer
    queryset = Category.objects.all()
