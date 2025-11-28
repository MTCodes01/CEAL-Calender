from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'club', 'notification_enabled', 'timezone', 'is_staff']
    list_filter = ['club', 'notification_enabled', 'is_staff', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Club & Notifications', {
            'fields': ('club', 'notification_enabled', 'notification_time', 'timezone', 'last_notification_sent_at')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'club')
        }),
    )
