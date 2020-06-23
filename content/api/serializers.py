from django.contrib.auth.models import User
from rest_framework import serializers
from content.models import Post


class UserSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(source='profile.get_sex_display', read_only=True)
    birth_date = serializers.CharField(source='profile.birth_date', read_only=True)
    rating = serializers.IntegerField(source='profile.rating', read_only=True)
    show_in_search_results = serializers.IntegerField(source='profile.rating', read_only=True)

    location = serializers.SerializerMethodField()

    def get_location(self, obj):
        if obj.profile.lat and obj.profile.lng:
            return [obj.profile.lat, obj.profile.lng]
        else:
            return None

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'sex', 'birth_date', 'rating',
                  'show_in_search_results', 'location')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Post
