from django.conf import settings
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser

from api.core.mixins import MultiSerializerViewSetMixin
from api.core.parsers import MultiPartJSONParser
from api.public.offer.serializers import OfferSerializer, RatingSerializer, PriceSerializer, \
    OfferCreateSerializer, OfferUpdateSerializer, BoardOfferSerializer
from offer.models import Offer, Price, Rating


class OfferViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """
    Класс для отображения информации о предложении (объявлении) в личном кабинете
    """

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    serializer_map = {
        'create': OfferCreateSerializer,
        'update': OfferUpdateSerializer
    }
    filter_backends = [SearchFilter]
    search_fields = ['product__category__name', 'rental_point__address__city__name', 'rental_point__company__name']
    parser_classes = (MultiPartJSONParser, JSONParser)
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES

    def get_queryset(self):
        return super().get_queryset().annotate(
            general_rating=Coalesce(Avg('ratings__mark'), Value(.0), output_field=FloatField()))


class BoardOfferViewSet(ModelViewSet):
    """
    Класс для отображения информации о предложении (объявлении) на доске объявлений
    """

    queryset = Offer.objects.all()
    serializer_class = BoardOfferSerializer
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class PriceViewSet(ModelViewSet):
    """
    Класс для отображения информации о стоимости предмета аренды
    """

    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES

    def perform_create(self, serializer):
        serializer.save(offer_id=self.kwargs.get('offer_pk'))


class RatingViewSet(ModelViewSet):
    """
    Класс для отображения инфомрации о рейтинге
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES

    def get_queryset(self):
        return super().get_queryset().filter(offer_id=self.kwargs.get('offer_pk'))

    def perform_create(self, serializer):
        serializer.save(offer_id=self.kwargs.get('offer_pk'))
