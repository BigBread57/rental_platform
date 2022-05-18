from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAdminUser

from api.auth.views import UserDetailsView, RegisterView

app_name = 'auth'

schema_view = get_schema_view(
    openapi.Info(
        title="API аутентификации",
        default_version='v1',
    ),
    patterns=[path('api/v1/auth/', include('api.auth.urls'))],
    public=True,
    permission_classes=(IsAdminUser,),
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('', include('rest_auth.urls')),
    path('', RegisterView.as_view())
]
