from rest_framework import serializers

from reference.models import Address, City, Category


class UserAddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор адреса пользователя
    """

    class Meta:
        model = Address
        fields = ('id', 'city',)
        read_only_fields = ('id',)


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор адреса пользователя
    """

    class Meta:
        model = City
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий предметов аренды
    """

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)
