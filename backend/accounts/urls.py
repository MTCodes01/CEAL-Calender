from django.urls import path
from django.urls import path
from .views import (
    RateLimitedTokenObtainPairView, SignupView, UserProfileView,
    ChangePasswordView, LogoutView, UserListView, UserDetailView,
    CookieTokenRefreshView, PasswordResetRequestView, PasswordResetConfirmView,
    VersionView
)

urlpatterns = [
    # JWT authentication
    path('login/', RateLimitedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    
    # User management
    path('signup/', SignupView.as_view(), name='signup'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Password Reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Admin endpoints (split into list + detail)
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('version/', VersionView.as_view(), name='version'),
]
