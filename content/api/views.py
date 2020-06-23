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
from content.models import Post
from .serializers import UserSerializer, PostSerializer


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
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def my_profile(self, request):
        serializer = self.serializer_class(instance=request.user, many=False)
        return Response(serializer.data)


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
