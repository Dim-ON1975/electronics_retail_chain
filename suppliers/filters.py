import django_filters
from .models import NetworkSupplier


class NetworkSupplierFilter(django_filters.FilterSet):
    """Фильтр по полю 'город' при условии точного совпадения запроса"""
    city = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = NetworkSupplier
        fields = ['city']
