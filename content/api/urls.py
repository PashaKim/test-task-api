from django.urls import include, path
from rest_framework import routers

from content.api.views import UserViewSet, PostViewSet, ObtainExpiringAuthToken

router = routers.DefaultRouter()

router.register('users', UserViewSet)
router.register('posts', PostViewSet),

urlpatterns = [
    path('', include(router.urls)),
    path('my_profile/', UserViewSet.as_view({'get': 'my_profile'}), name='my_profile'),
    path('auth/', include('rest_framework.urls')),  # login, logout
    path('token/', ObtainExpiringAuthToken.as_view(), name='my_profile')
]
