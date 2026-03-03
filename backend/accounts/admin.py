from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from .models import User
from events.models import Event
from notifications.tasks import send_digest_email


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'club', 'notification_enabled', 'timezone', 'is_staff']
    list_filter = ['club', 'notification_enabled', 'is_staff', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    actions = ['send_test_notification']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Club & Notifications', {
            'fields': ('club', 'sub_club', 'notification_enabled', 'notification_time', 'timezone', 'last_notification_sent_at')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'club', 'sub_club')
        }),
    )

    @admin.action(description='Send Test Notification (Last 5 Events)')
    def send_test_notification(self, request, queryset):
        success_count = 0
        for user in queryset:
            if not user.club:
                continue
                
            # Get last 5 events for the user's club regardless of creation time
            effective_club_id = user.sub_club_id if user.sub_club_id else user.club_id
            recent_events = Event.objects.filter(club_id=effective_club_id).order_by('-created_at')[:5]
            
            if recent_events.exists():
                events_list = list(recent_events)
                if send_digest_email(user, events_list):
                    success_count += 1
                    
        self.message_user(request, f'Successfully sent test notifications to {success_count} user(s).')
