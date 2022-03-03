from django import forms
import django_filters
from .models import Maker_company, Record_block, Component, Record_component, Defect_statement, Maker, Type_block, Order


class One_block_filter(django_filters.FilterSet):
    number_block = django_filters.NumberFilter()
    maker = django_filters.ModelChoiceFilter( queryset=Maker_company.objects.all(),
        field_name='Производитель', method='get_maker', label="Производитель")

    def get_maker(self, queryset, field_name, value):
        return queryset.filter(name_block__maker=value)

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
    maker = django_filters.ModelChoiceFilter( queryset=Maker_company.objects.all(),
        field_name='Производитель', method='get_maker', label="Производитель")

    def get_maker(self, queryset, field_name, value):
        return queryset.filter(name_block__maker=value)

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


class Maker_filter(django_filters.FilterSet):
    number_block = django_filters.RangeFilter()
    name_block = django_filters.ModelChoiceFilter(
        label="Наименование блока",
        queryset=Type_block.objects.all(),
    )
    serial_number = django_filters.CharFilter(
        lookup_expr='icontains',
        method='get_serial_number',
    )
    date_add_maker = django_filters.DateFromToRangeFilter()
    date_shipment_maker = django_filters.DateFromToRangeFilter()

    def get_serial_number(self, queryset, field_name, value):
        return queryset.filter(block__serial_number=value)
    
    class Meta:
        model = Maker
        fields = ("__all__")


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


class Defect_filter(django_filters.FilterSet):
    class Meta:
        model = Defect_statement
        fields = (
            'region',
            'date_add',
        )

    
class Order_filter(django_filters.FilterSet):
    date_commit = django_filters.DateFromToRangeFilter()
    date_created = django_filters.DateFromToRangeFilter()
    date_processing = django_filters.DateFromToRangeFilter()
    date_order = django_filters.DateFromToRangeFilter()
    delivery_time = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Срок поставки',
    )
    invoice_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Номер счета',
    )
    provider = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Поставщик',
    )
    user = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Фамилия',
    )
    class Meta:
        model = Order
        fields = ('__all__')