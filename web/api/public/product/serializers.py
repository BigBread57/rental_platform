from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор предмета аренды
    """

    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ('id', 'category', 'name')
        read_only_fields = ('id',)
