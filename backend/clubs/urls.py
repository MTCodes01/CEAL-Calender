from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClubListView, ClubManagementViewSet

router = DefaultRouter()
router.register('manage', ClubManagementViewSet, basename='club-manage')

urlpatterns = [
    path('', ClubListView.as_view(), name='club-list'),
    path('', include(router.urls)),
]
