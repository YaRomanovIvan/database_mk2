import django_filters
from .models import Record_block


class One_block_filter(django_filters.FilterSet):
    number_block = django_filters.NumberFilter()

    class Meta:
        model = Record_block
        fields = [
            'number_block',
            'name_block',
            'serial_number',
            'date_add',
            'date_repair',
            'date_shipment',
            'region',
            'FIO',
            'status',
        ]


class Block_filter(django_filters.FilterSet):
    number_block = django_filters.RangeFilter()
    serial_number = django_filters.CharFilter(
        lookup_expr='icontains',
    )
    date_add = django_filters.DateFromToRangeFilter()
    date_repair = django_filters.DateFromToRangeFilter()
    date_shipment = django_filters.DateFromToRangeFilter()
    FIO = django_filters.CharFilter(
        lookup_expr='icontains',
    )

    class Meta:
        model = Record_block
        fields = [
            'number_block',
            'name_block',
            'serial_number',
            'date_add',
            'date_repair',
            'date_shipment',
            'region',
            'FIO',
            'status',
        ]