from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from content.api.filters import BirthDateFilter, LocationFilter, RatingFilter, SexFilter
from content.models import Post, PostEditHistory
from .serializers import UserSerializer, PostSerializer, PostEditHistorySerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ['get']
    permission_classes = (IsAuthenticated, )
    filter_backends = (BirthDateFilter,
                       LocationFilter,
                       RatingFilter,
                       SexFilter
                       )

    @action(detail=True, methods=['get'],)
    def posts_list(self, request, pk,):
        user = get_object_or_404(User, pk=pk)
        posts = Post.objects.filter(author_id=user.id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def my_profile(self, request):
        serializer = self.serializer_class(instance=request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = ()

    @action(detail=True, methods=['post'], )
    def creating(self, request):  # create is forbidden
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'], )
    def edit(self, request, pk, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Post.objects.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['delete'],)
    def delete(self, request, pk):
        instance = Post.objects.get(pk=pk)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], )
    def history(self, request, pk,):
        post = get_object_or_404(Post, pk=pk)
        histories = PostEditHistory.objects.filter(post_id=post.id)
        serializer = PostEditHistorySerializer(histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.utcnow()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
