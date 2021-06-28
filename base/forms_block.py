from django import forms
from django.forms.widgets import Widget
from .models import Components, Type_block, Unit, Record_block


class Type_block_form(forms.ModelForm):
    name_block = forms.CharField(
        label="Наименование блока",
        help_text='Например "Плата драйвера ДТИ 6/12 СМПК.758725.026"',
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-sm"}
        ),
    )
    components = forms.ModelMultipleChoiceField(
        queryset=Components.objects.all(),
        label='Привязать компоненты',
        help_text='Поле не обязательно для заполнения. Вы можете привязать компоненты позже.',
        widget=forms.SelectMultiple(attrs={"id": "id_record_component", "class": "form-control form-control-sm component_multiple_select2",}),
        required=False,
    )

    class Meta:
        model = Type_block
        fields = ("id", "name_block", "components",)


class Unit_form(forms.ModelForm):
    region = forms.CharField(
        label="Наименование участка",
        help_text='Например "Москва-Киевская"',
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-sm"}
        ),
    )

    class Meta:
        model = Unit
        fields = ("id", "region")


class Record_block_form(forms.ModelForm):
    number_block = forms.IntegerField(
        label="Номер блока",
        widget=forms.NumberInput(
            attrs={"class": "form-control form-control-sm"}
        ),
    )
    name_block = forms.ModelChoiceField(
        label="Наименование блока",
        queryset=Type_block.objects.all(),
        widget=forms.Select(attrs={"id": "id_record_block", "class": "form-control form-control-sm",}),
    )
    serial_number = forms.CharField(
        label="Заводской номер",
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-sm"}
        ),
        required=False,
    )
    region = forms.ModelChoiceField(
        label="Участок",
        queryset=Unit.objects.all(),
        widget=forms.Select(attrs={"class": "form-control form-control-sm"}),
    )

    class Meta:
        model = Record_block
        fields = ("number_block", "name_block", "serial_number", "region")


class Send_block_form(forms.ModelForm):
    passed = forms.CharField(
        label="Водитель",
        help_text='Петро В.В."',
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-sm"}
        ),
    )
    class Meta:
        model = Record_block
        fields = ("passed",)