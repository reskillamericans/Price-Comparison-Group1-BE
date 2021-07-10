from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *


@admin.register(User)
class MyUserAdmin(BaseUserAdmin):
    """
    Used to customize User tables on admin site.
    """

    fieldsets = (
        ('Required', {'fields': ('username', 'password', 'email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        )

    list_display = ('username', 'email', 'is_active', 'is_staff', 'last_login')


# Unregister default User model from admin site
admin.site.unregister(User)

# Register new User model and apply table customizations
admin.site.register(User, MyUserAdmin)
