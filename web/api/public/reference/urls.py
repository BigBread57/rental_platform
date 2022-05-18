from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from api.public.reference.views import UserAddressListApiView, CityListApiView, CategoryViewSet, ProductViewSet

app_name = 'reference'


router = SimpleRouter()
router.register('category', CategoryViewSet)

nested_router = NestedSimpleRouter(router, 'category', lookup='category')
nested_router.register('product', ProductViewSet)


urlpatterns = [
    path('city/', CityListApiView.as_view(), name='city'),
    path('address/', UserAddressListApiView.as_view(), name='address'),
    *nested_router.urls,
    *router.urls,
]
