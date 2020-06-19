from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response

from content.api.filters import BirthDateFilter
from content.models import CustomUser as User, Post
from .serializers import UserSerializer, PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['get']
    filter_backends = (BirthDateFilter,
                       )

    @action(detail=True, methods=['get'])
    def user_posts_list(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        posts = Post.objects.filter(author_id=user.id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
