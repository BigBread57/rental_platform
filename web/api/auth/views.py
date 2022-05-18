from django.conf import settings
from rest_auth.registration.views import RegisterView as DefaultRegisterView
from rest_auth.views import UserDetailsView as BaseUserDetailsView
from rest_framework.permissions import IsAuthenticated


from api.auth.serializers import UserDetailsSerializer, RegisterSerializer


class UserDetailsView(BaseUserDetailsView):
    """
    Класс переопределяет serializer, который отвечает за профиль пользователя
    """

    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES


class RegisterView(DefaultRegisterView):

    serializer_class = RegisterSerializer

