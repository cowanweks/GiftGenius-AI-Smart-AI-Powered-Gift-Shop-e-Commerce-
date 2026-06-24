import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    occasion = django_filters.CharFilter(field_name='occasion', lookup_expr='exact')
    gender = django_filters.CharFilter(field_name='gender', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category', 'occasion', 'gender', 'min_price', 'max_price']
