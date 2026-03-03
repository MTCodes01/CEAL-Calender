from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RateLimitedTokenObtainPairView, SignupView, UserProfileView,
    ChangePasswordView, LogoutView, UserListView, UserDetailView,
)

urlpatterns = [
    # JWT authentication
    path('login/', RateLimitedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User management
    path('signup/', SignupView.as_view(), name='signup'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Admin endpoints (split into list + detail)
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
