import jwt
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from .models import CustomUser


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = None
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256'],
                )
                user_id = payload.get('user_id')
                if user_id:
                    try:
                        user = CustomUser.objects.get(
                            id=user_id,
                            is_active=True,
                        )
                        request.user = user
                    except CustomUser.DoesNotExist:
                        pass
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                pass
