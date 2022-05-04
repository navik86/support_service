
from django.contrib import admin

from .models import User, UserGroup


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'group', 'support')


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
