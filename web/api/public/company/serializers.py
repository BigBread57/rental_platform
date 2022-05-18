from rest_framework import serializers

from api.core.serializers import ChoiceField, SimpleNameSerializer
from company.models import Company, RentalPoint, Reservation
from core.collections import ReservationStatuses
from offer.models import Offer, Rating, Price
from reference.models import Address


class PointAddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор адреса точки выдачи
    """

    city_name = serializers.CharField(label='Название города', source='city.name', read_only=True)

    class Meta:
        model = Address
        fields = ('id', 'city', 'city_name', 'address', 'latitude', 'longitude')
        read_only_fields = ('id',)


class CreateRentalPointSerializer(serializers.ModelSerializer):
    """
    Сериализатор точки выдачи
    """
    
    address = PointAddressSerializer(label='Адрес')

    class Meta:
        model = RentalPoint
        fields = ('id', 'phone', 'is_delivery', 'address')
        read_only_fields = ('id',)

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)

        validated_data.update({
            'address': address
        })

        return super().create(validated_data)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address
        Address.objects.filter(id=address.id).update(**address_data)

        instance.refresh_from_db()

        return super().update(instance, validated_data)


class CompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор компании
    """

    rental_points = CreateRentalPointSerializer(label='Точки выдачи', many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'rental_points')
        read_only_fields = ('id',)


class BoardCompanySerializer(serializers.ModelSerializer):
    """
    Сериализатор всех компаний
    """

    rental_points = CreateRentalPointSerializer(label='Точки выдачи', many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'rental_points')
        read_only_fields = fields


class ReservationSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для бронирования предметов аренды для пользователя
    """

    status = ChoiceField(choices=ReservationStatuses.CHOICES, required=False)

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('id', 'date_created', 'user', 'offer')


class RentalPointReadOnlySerializer(serializers.ModelSerializer):
    """
    Сериалайзер для предоставления списка филиалов
    """

    address = PointAddressSerializer(label='Адрес')
    general_rating = serializers.SerializerMethodField()

    class Meta:
        model = RentalPoint
        fields = ('id', 'phone', 'is_delivery', 'address', 'general_rating')
        read_only_fields = ('id',)

    def get_general_rating(self, obj):
        return round(obj.general_rating, 2)


class RatingReadOnlySerializer(serializers.ModelSerializer):
    """
    Сериализатор рейтинга
    """

    class Meta:
        model = Rating
        fields = ('id', 'mark', 'comment')
        read_only_fields = fields


class PriceReadOnlySerializer(serializers.ModelSerializer):
    """
    Сериализатор цены
    """

    time_from_unit_display = serializers.SerializerMethodField()
    price_per_time_unit_display = serializers.SerializerMethodField()

    class Meta:
        model = Price
        fields = ('id', 'time_from', 'time_from_unit', 'time_from_unit_display', 'price_per_time', 'price_per_time_unit',
                  'price_per_time_unit_display')
        read_only_fields = fields

    def get_time_from_unit_display(self, obj):
        return obj.get_time_from_unit_display()

    def get_price_per_time_unit_display(self, obj):
        return obj.get_price_per_time_unit_display()


class OfferReadOnlySerializer(serializers.ModelSerializer):
    """
    Сериализатор предложений
    """

    rating = RatingReadOnlySerializer(source='ratings', many=True, read_only=True)
    price = PriceReadOnlySerializer(source='prices', many=True, read_only=True)
    product = SimpleNameSerializer(label='Предмет', read_only=True)
    category = SimpleNameSerializer(label='Категория', source='product.category', read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'is_active', 'description', 'count', 'is_for_child', 'is_female', 'is_male', 'is_unisex',
                  'product', 'category', 'price', 'rating')
        read_only_fields = fields


class ReservationsReadOnlySerializer(ReservationSerializer):
    """
    Сериализатор бронирований
    """

    class Meta:
        model = Reservation
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            field.read_only = True

        return fields
