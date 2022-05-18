import json

import requests

from django.conf import settings
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from django.utils.functional import cached_property
from rest_framework import mixins, exceptions as drf_exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.core.mixins import MultiSerializerViewSetMixin
from api.public.company.serializers import CompanySerializer, CreateRentalPointSerializer, \
    ReservationSerializer, BoardCompanySerializer, RentalPointReadOnlySerializer, OfferReadOnlySerializer, \
    ReservationsReadOnlySerializer

from company.models import Company, RentalPoint, Reservation
from core.collections import ReservationStatuses
from offer.models import Offer


class CompanyViewSet(ModelViewSet):
    """
    Набор представлений компании
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES

    def get_object(self):
        return self.get_queryset().filter(user=self.request.user).first()

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def perform_create(self, serializer):
        if self.request.user.company:
            raise drf_exceptions.ValidationError('У пользователя уже есть компания.')

        serializer.save(user=self.request.user)


class BoardCompanyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Набор всех компаний
    """

    permission_classes = (AllowAny,)
    queryset = Company.objects.all()
    serializer_class = BoardCompanySerializer


class RatingMixin:
    """
    Примесь для добавления среднего значения рейтинга к компаниям
    """
    def get_queryset(self):
        return super().get_queryset().annotate(
            general_rating=Coalesce(Avg('offers__ratings__mark'), Value(.0), output_field=FloatField()))


class CompanyRentalPointViewSet(MultiSerializerViewSetMixin, RatingMixin, ModelViewSet):
    """
    Набор представлений точки
    """

    queryset = RentalPoint.objects.all()
    serializer_class = CreateRentalPointSerializer
    serializer_map = {
        'retrieve': RentalPointReadOnlySerializer,
        'list': RentalPointReadOnlySerializer
    }
    permission_classes = (IsAuthenticated,)
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES

    def get_queryset(self):
        return super().get_queryset().filter(company_id=self.kwargs.get('company_pk'))

    def perform_create(self, serializer):
        serializer.save(company_id=self.kwargs.get('company_pk'))


class RentalPointViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, RatingMixin, GenericViewSet):
    """
    Класс отображения информации о всех филиалах
    """

    queryset = RentalPoint.objects.all()
    serializer_class = RentalPointReadOnlySerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES


class RentalPointOffersViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Класс отображения информации о предложениях филиала
    """

    queryset = Offer.objects.all()
    serializer_class = OfferReadOnlySerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES
    rental_point_pk_field = 'rental_point_pk'

    @cached_property
    def rental_point(self):
        return get_object_or_404(RentalPoint.objects.all(), pk=self.kwargs.get(self.rental_point_pk_field))

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_queryset()

        return super().get_queryset().filter(rental_point=self.rental_point)


class ReservationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                         mixins.CreateModelMixin, GenericViewSet):
    """
    Класс бронирования предметов в объявлении
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES

    def perform_create(self, serializer):
        """
        При создании пользователь указывает количетсво забронированного инвентаря.
        В объявление количество не уменьшается, потому что заявка имеет статус новая и не подтверждена
        """

        offer = Offer.objects.get(id=self.kwargs.get('offer_pk'))
        serializer.save(user=self.request.user, offer=offer)

    def perform_update(self, serializer):
        """
        Редактирование брони
        """

        instance = serializer.instance
        offer = instance.offer
        reservation_count = serializer.validated_data.get('count') or instance.count
        new_status = serializer.validated_data.get('status', ReservationStatuses.NEW)

        if new_status == ReservationStatuses.ACCEPTED:
            if offer.count >= reservation_count:
                offer.count -= reservation_count
                offer.save()
            else:
                raise drf_exceptions.ValidationError('Недостаточно в наличии.')

        elif new_status in (ReservationStatuses.NEW, ReservationStatuses.DONE, ReservationStatuses.DECLINED,
                            ReservationStatuses.CANCELED):
            if instance.status == ReservationStatuses.ACCEPTED:
                offer.count += reservation_count
                offer.save()

        serializer.save()


class RentalPointReservationsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    Класс отображения информации о бронированиях филиала
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationsReadOnlySerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES
    rental_point_pk_field = 'rental_point_pk'

    @cached_property
    def rental_point(self):
        return get_object_or_404(RentalPoint.objects.all(), pk=self.kwargs.get(self.rental_point_pk_field))

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_queryset()

        return super().get_queryset().filter(offer__rental_point=self.rental_point)


# TODO: Изменить прокси-представление после готовности сервиса расписания
class SlotsAPIView(APIView):
    """
    Представление для проксирования запросов по слотам к сервису слотов
    """

    http_method_names = settings.ALLOWED_HTTP_METHOD_NAMES

    def get(self, request, *args, **kwargs):
        response = requests.get(url=f'{settings.HOST_OFFER}/api/slots/12/2021-05-22')

        return Response(data=response.json())

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        response = requests.post(url=f'{settings.HOST_OFFER}/resolveSlots', json=data)

        return Response(data=response)
