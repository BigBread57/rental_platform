import django_filters as filters

from offer.models import Offer


class OfferFilterSet(filters.FilterSet):
    """
    Набор фильтров предложений
    """

    category = filters.CharFilter(label='Категория', lookup_expr='icontains', field_name='product__category__name')
    city = filters.CharFilter(label='Город', lookup_expr='icontains', field_name='rental_point__address__city__name')
    company = filters.CharFilter(label='Компания', lookup_expr='icontains', field_name='rental_point__company__name')

    class Meta:
        model = Offer
        fields = ('category', 'city', 'company')
