from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAdminUser


app_name = 'public'

schema_view = get_schema_view(
    openapi.Info(
        title="API публичного доступа",
        default_version='v1',
    ),
    patterns=[path('api/v1/', include('api.public.urls'))],
    public=True,
    permission_classes=(IsAdminUser,),
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
    path('company/', include('api.public.company.urls', namespace='company')),
    path('reference/', include('api.public.reference.urls', namespace='reference')),
    path('product/', include('api.public.product.urls', namespace='product')),
    path('offer/', include('api.public.offer.urls', namespace='offer')),
]
