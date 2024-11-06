from django.contrib.auth import user_logged_in
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

from .serializer import LoginSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        if not serializer.errors:
            user = serializer.validated_data['user']
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            result = super().post(request, *args, **kwargs)
            result.set_cookie('AuthToken', serializer.validated_data['user'].auth_token.key)
            return result
        return Response(
            {'detail': 'Неверные логин или пароль'},
            status=HTTP_403_FORBIDDEN
        )
