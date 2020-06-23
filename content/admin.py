from django.contrib import admin
from datetime import datetime
from .models import Profile, Post, PostEditHistory


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sex', 'birth_date', 'rating', 'show_in_search_results')
    readonly_fields = ('rating', 'show_in_search_results')
    search_fields = ('user__username', 'user__last_name')
    raw_id_fields = ('user',)
    list_filter = ('sex', )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created', 'updated')
    readonly_fields = ('created', 'updated',)  # add 'author', 'text' for security
    raw_id_fields = ('author',)


@admin.register(PostEditHistory)
class PostEditHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'post_id', 'author', 'updated')
    readonly_fields = ('post', 'author', 'text', 'timestamp')

    def updated(self, obj):
        return datetime.fromtimestamp(obj.timestamp)
