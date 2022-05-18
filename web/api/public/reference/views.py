from django.conf import settings
from django.utils.functional import cached_property
from rest_framework import mixins
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from api.core.serializers import SimpleNameSerializer
from api.public.reference.serializers import UserAddressSerializer, CitySerializer, CategorySerializer
from product.models import Product
from reference.models import Address, City, Category


class UserAddressListApiView(ListAPIView):
    """
    Класс позволяет отображать информацию об адресе пользователя
    """

    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES
    permission_classes = (AllowAny,)


class CityListApiView(ListAPIView):
    """
    Класс возвращает список городов
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES
    permission_classes = (AllowAny,)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Класс отображает информацию о категориях
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES
    permission_classes = (AllowAny,)


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Набор представлений для предметов аренды
    """

    queryset = Product.objects.all()
    serializer_class = SimpleNameSerializer
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES
    permission_classes = (AllowAny,)
    category_pk_field = 'category_pk'

    @cached_property
    def category(self):
        return get_object_or_404(Category.objects.all(), pk=self.kwargs.get(self.category_pk_field))

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_queryset()

        return super().get_queryset().filter(category=self.category)
