from rest_framework import serializers

from api.core.serializers import ChoiceField
from api.public.company.serializers import CreateRentalPointSerializer
from core.collections import TimeUnits
from offer.models import Offer, Price, Rating, OfferImage


class PriceSerializer(serializers.ModelSerializer):
    """
    Сериализатор предложений (объявлений)
    """

    time_from_unit = ChoiceField(choices=TimeUnits.CHOICES)
    price_per_time_unit = ChoiceField(choices=TimeUnits.CHOICES)

    class Meta:
        model = Price
        fields = ('id', 'time_from', 'time_from_unit', 'price_per_time', 'price_per_time_unit', 'offer')
        read_only_fields = ('id',)


class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рейтинга
    """

    class Meta:
        model = Rating
        fields = ('id', 'mark', 'comment', 'offer', 'user')
        read_only_fields = ('id',)


class BoardOfferSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка объявлений
    """

    rental_point = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ('id', 'is_active', 'description', 'count', 'product', 'rental_point')
        read_only_fields = fields

    def get_rental_point(self, obj):

        return f'{obj.rental_point.address}'


class OfferSerializer(serializers.ModelSerializer):
    """
    Сериализатор просомтра предложений (объявлений) в личном кабинете
    """

    rental_point = CreateRentalPointSerializer()
    rating = RatingSerializer(source='ratings', many=True)
    general_rating = serializers.SerializerMethodField()
    price = PriceSerializer(source='prices', many=True)
    product = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ('id', 'is_active', 'description', 'count', 'is_for_child', 'is_female', 'is_male', 'is_unisex',
                  'product', 'price', 'rental_point', 'general_rating', 'rating')
        read_only_fields = fields

    def get_general_rating(self, obj):
        return round(obj.general_rating, 2)

    def get_product(self, obj):
        return obj.product.name if obj.product else None


class OfferImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор изображения
    """

    image_url = serializers.URLField(label='URL изображения', source='image.url', read_only=True)

    class Meta:
        model = OfferImage
        fields = ('id', 'name', 'image_url')
        read_only_fields = fields


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания предложений (объявлений)
    """

    images = OfferImageSerializer(label='Изображения', many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'is_active', 'description', 'count', 'is_for_child', 'is_female', 'is_male', 'is_unisex',
                  'product', 'rental_point', 'images')
        read_only_fields = ('id',)

    def create(self, validated_data):

        instance = super().create(validated_data)

        images_data = self.initial_data.get('images')

        if images_data:
            images = OfferImage.objects.bulk_create([
                OfferImage(image=image, name=image.name) for image in images_data
            ])
            instance.images.set(images)

        return instance


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор редактирования предложений (объявлений)
    """

    images = OfferImageSerializer(label='Изображения', many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'is_active', 'description', 'count', 'is_for_child', 'is_female', 'is_male', 'is_unisex',
                  'product', 'rental_point', 'images')
        read_only_fields = ('id',)
        extra_kwargs = {
            'count': {'required': False},
            'rental_point': {'required': False}
        }

    def update(self, instance, validated_data):

        images_data = self.initial_data.get('images')

        if images_data:
            images = OfferImage.objects.bulk_create([
                OfferImage(image=image, name=image.name) for image in images_data
            ])
            instance.images.set(images)

        return super().update(instance, validated_data)

