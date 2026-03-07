import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import (
    SignupSerializer, UserSerializer, UserSettingsSerializer,
    ChangePasswordSerializer, AdminUserUpdateSerializer,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Auth-specific throttle (stricter than global default)
# ---------------------------------------------------------------------------
class AuthRateThrottle(ScopedRateThrottle):
    scope = 'auth'


# ---------------------------------------------------------------------------
# Authentication Views
# ---------------------------------------------------------------------------
class RateLimitedTokenObtainPairView(TokenObtainPairView):
    """
    Login endpoint with stricter rate limiting to prevent brute-force attacks.
    """
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs):
        logger.info("Login attempt for email: %s", request.data.get('email', 'unknown'))
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            logger.info("Login successful for email: %s", request.data.get('email'))
        return response


class SignupView(generics.CreateAPIView):
    """
    User registration endpoint with rate limiting.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer
    throttle_classes = [AuthRateThrottle]

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info("New user registered: %s (id=%s)", user.email, user.id)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update current user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserSettingsSerializer
        return UserSerializer


class ChangePasswordView(APIView):
    """
    Change user password.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.data.get('new_password'))
            user.save()
            logger.info("Password changed for user: %s", user.email)
            
            return Response(
                {"message": "Password updated successfully."},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout endpoint (blacklist refresh token).
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out: %s", request.user.email)
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.warning("Logout failed for user %s: %s", request.user.email, str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------
# Admin Views (split from the broken multi-inherited UserViewSet)
# ---------------------------------------------------------------------------
class UserListView(generics.ListAPIView):
    """
    Admin endpoint to list all users.
    """
    queryset = User.objects.select_related('club', 'sub_club').prefetch_related('extra_clubs').all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin endpoint to retrieve, update, or delete a single user.
    """
    queryset = User.objects.select_related('club', 'sub_club').prefetch_related('extra_clubs').all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return AdminUserUpdateSerializer
        return UserSerializer

    def perform_destroy(self, instance):
        logger.warning("Admin %s deleted user %s (id=%s)", self.request.user.email, instance.email, instance.id)
        instance.delete()
