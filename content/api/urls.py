from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from rest_framework import routers

from content.api.views import UserViewSet

router = routers.DefaultRouter()

router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user_posts_list/<int:pk/>', UserViewSet.as_view({'get': 'user_posts_list'})),
    path('login/', auth_views.obtain_auth_token)
]