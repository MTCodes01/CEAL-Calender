"""
URL configuration for ceal_calendar project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/clubs/', include('clubs.urls')),
    path('api/events/', include('events.urls')),
]
