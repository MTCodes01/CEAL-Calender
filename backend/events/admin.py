from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'location', 'start', 'end', 'created_by', 'created_at']
    list_filter = ['club', 'start', 'created_at']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'location')
        }),
        ('Schedule', {
            'fields': ('start', 'end')
        }),
        ('Relations', {
            'fields': ('club', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
