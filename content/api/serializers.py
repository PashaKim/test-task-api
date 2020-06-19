from django.contrib.auth import authenticate
from rest_framework import serializers
from content.models import CustomUser as User, Post, CustomToken


class UserSerializer(serializers.ModelSerializer):
    sex_display = serializers.CharField(source='get_sex_display', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'sex', 'sex_display', 'birth_date', 'rating',
                  'show_in_search_results', 'lat', 'lng')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Post
