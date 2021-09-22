from django import forms
import django_filters
from .models import Record_block, Component, Record_component


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


class Components_filter(django_filters.FilterSet):
    type_component = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Тип компонента',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'стабилизатор/микросхема/транзистор и т.п.'
            }
        ),
    )
    marking = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Маркировка',
        widget=forms.TextInput(
            attrs={
                'placeholder': '78L05/LTO100F20R/IRF640N и т.п.'
            }
        )
    )
    amount_eis = django_filters.RangeFilter(
        label='Количество ЭИС',
    )
    amount_trk = django_filters.RangeFilter(
        label='Количество ТРК',
    )
    amount_vts = django_filters.RangeFilter(
        label='Количество ВТС',
    )
    summ = django_filters.RangeFilter(
        label='Общее количество',
    )
    price = django_filters.RangeFilter(
        label='Цена',
    )

    class Meta:
        model = Component
        fields = (
            'type_component',
            'marking',
            'amount_eis',
            'amount_trk',
            'amount_vts',
            'summ',
            'price',
        )


class Record_components_filter(django_filters.FilterSet):
    date_add = django_filters.DateFromToRangeFilter()
    component = django_filters.ModelMultipleChoiceFilter(
        queryset=Component.objects.all()
    )
    class Meta:
        model = Record_component
        fields = (
            'component',
            'company',
            'date_add',
        )