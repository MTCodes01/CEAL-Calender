from django.urls import path
from .views import ClubListView

urlpatterns = [
    path('', ClubListView.as_view(), name='club-list'),
]
