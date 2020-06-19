from django.contrib import admin
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, CustomToken, Post, PostEditHistory


class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'birth_date', 'sex', 'lat', 'lng')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'birth_date', 'sex', 'lat', 'lng')}),
         )
    fieldsets = UserAdmin.fieldsets + ((_('Custom info'), {'fields': ('birth_date', 'sex', 'lat', 'lng')}),)

    list_display = ('id', 'username', 'last_name', 'first_name', 'sex', 'birth_date', 'rating', 'show_in_search_results')
    readonly_fields = ('rating', 'show_in_search_results')
    search_fields = ('username', 'last_name')
    list_filter = ('sex', )


@admin.register(CustomToken)
class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created')
    readonly_fields = ('user', 'key', 'created')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created', 'updated')
    readonly_fields = ('created', 'updated',)  # add 'author', 'text' for security
    raw_id_fields = ('author',)


@admin.register(PostEditHistory)
class PostEditHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'updated')
    readonly_fields = ('post', 'author', 'text', 'timestamp')

    def updated(self, obj):
        return datetime.fromtimestamp(obj.timestamp)
