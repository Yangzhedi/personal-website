import datetime

from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404

from .models import Post
from .serializers import PostSerializer, PostDetailSerializer


# @api_view()
# def post_list(request):
#     posts = Post.objects.filter(status=Post.STATUS_NORMAL)
#     post_serializers = PostSerializer(posts, many=True)
#     return Response(post_serializers.data)
#
#
# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
#     serializer_class = PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # permission_classes = [IsAdminUser]
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'list': [AllowAny],
        'retrieve': [AllowAny]
    }

    # read
    # GET /api/post/{id}/
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    # create
    # POST /api/post/
    def create(self, request, *args, **kwargs):
        return super(PostViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(PostViewSet, self).list(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class PostLatestViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    def latest(self, request):
        post = Post.objects.latest('id')
        serializer = self.get_serializer(post)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def post_test_list(request):
    permission_classes = [AllowAny]
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # print(request.data)
        # serializer = PostSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.latest('id')
        # print(post)
        serializer = PostDetailSerializer(post)
        # serializer = self.get_serializer(post)
        return Response(serializer.data)


@api_view(['POST'])
def get_post_by_url(request):
    permission_classes = [AllowAny]
    """
    List all code snippets, or create a new snippet.
    """
    req = request.data
    year = request.data['year']
    month = request.data['month']
    print(req['year'], req['month'])
    # post = Post.objects.latest('id')
    # post = Post.objects.filter(create_time__year=req['year'])[:1].get()
    # postQuerySet = Post.objects.filter(create_time__year=req['year']) \
    #     .filter(create_time__month=req['month']) \
    #     .filter(url=req['url'])

    day_max = 30
    months = [1, 3, 5, 7, 8, 10, 12]
    if int(month) in months:
        day_max = 31

    post_query_set = Post.objects.filter(
        create_time__range=(datetime.date(int(year), int(month), 1), datetime.date(int(year), int(month), day_max))
    ).filter(url=req['url'])

    print(len(post_query_set))

    # post = Post.objects.get(create_time__year=req['year'], create_time__month=req['month'])

    post = get_object_or_404(post_query_set)
    # print(post)
    serializer = PostDetailSerializer(post)
    # serializer = self.get_serializer(post)
    return Response(serializer.data)