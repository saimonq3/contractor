from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {
            'fields': (
                'password',
            )
        }),
        (_('Personal info'), {
            'fields':
                (
                    'first_name',
                    'last_name',
                    'email',
                    'email_verified',
                    'sex',
                    'phone_number',
                    'country_code',
                    'uuid',
                    'id',
                    'avatar',
                )
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'last_name', 'sex', 'password1', 'password2',
                       'is_staff'),
        }),
    )

    list_display = [
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'country_code',
        'id',
        'is_staff',
        'date_joined',
    ]
    list_filter = [
        'is_staff'
    ]
    readonly_fields = [
        'id',
        'uuid',
        'last_login',
        'date_joined',
    ]
    ordering = [
        '-is_staff',
    ]
    search_fields = [
        'id',
        'uuid',
        'first_name',
        'last_name',
        'email',
        'phone_number',
    ]
