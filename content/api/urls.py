from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from rest_framework import routers

from content.api.views import UserViewSet, ObtainExpiringAuthToken

router = routers.DefaultRouter()

router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user_posts_list/<int:pk/>', UserViewSet.as_view({'get': 'posts_list'}), name='user_posts_list'),
    path('my_profile/', UserViewSet.as_view({'get': 'my_profile'}), name='my_profile'),
    path('token/', ObtainExpiringAuthToken.as_view(), name='my_profile')
]
