from django.conf import settings
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.public.product.serializers import ProductSerializer
from product.models import Product


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Класс отображает инфомрацию о предмете аренды
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES
