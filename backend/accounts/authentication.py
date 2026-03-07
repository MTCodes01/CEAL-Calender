from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that allows SimpleJWT to authenticate 
    an access token from an HttpOnly cookie.
    """
    def authenticate(self, request):
        # 1. First try the standard Authorization header mechanism (for testing/API clients)
        header_auth = super().authenticate(request)
        if header_auth is not None:
            return header_auth
            
        # 2. If no header, try to extract the access token from cookies
        access_token = request.COOKIES.get('access_token')
        
        if access_token is None:
            return None
            
        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token
