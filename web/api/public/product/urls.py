from rest_framework import routers

from api.public.product.views import ProductViewSet


app_name = 'product'


router = routers.SimpleRouter()


router.register('', ProductViewSet, basename='product')


urlpatterns = [
    *router.urls
]
