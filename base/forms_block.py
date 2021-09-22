from typing import DefaultDict
from django import forms
from .models import Component, Type_block, Unit, Record_block, Defect_statement


class Type_block_form(forms.ModelForm):
    name_block = forms.CharField(
        label="Наименование блока",
        help_text='Например "Плата драйвера ДТИ 6/12 СМПК.758725.026"',
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-sm"}
        ),
    )
    components = forms.ModelMultipleChoiceField(
        queryset=Component.objects.all(),
        label='Привязать компоненты',
        help_text='Поле не обязательно для заполнения. Вы можете привязать компоненты позже.',
        widget=forms.SelectMultiple(attrs={
            "id": "id_record_component", 
            "class": "component_multiple_select2",}),
        required=False,
    )

    class Meta:
        model = Type_block
        fields = ("id", "name_block", "components", "maker")


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
        fields = ("__all__")


class Send_block_form(forms.ModelForm):
    passed = forms.CharField(
        label="Водитель",
        help_text='Петров В.В."',
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-sm"}
        ),
    )
    class Meta:
        model = Record_block
        fields = ("passed",)


class Repair_block_form(forms.Form):
    components = forms.ChoiceField(
        required=False,
        label="Наименование компонента",
        widget=forms.Select(attrs={"class": "form-control form-control-sm", "id": "id_name_component",}),
    )
    amount = forms.IntegerField(
        required=False,
        label='Количество',
        widget=forms.NumberInput(
            attrs={"class": "form-control form-control-sm",  "id": "id_amount_component", "value": "1"}
        ),
    )
    note = forms.CharField(
        label="Примечание",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-sm"}
        ),
    )


class Defect_statement_form(forms.ModelForm):
    defect_2 = forms.CharField(
        required=False,
        label="Неисправность 2",
    )
    defect_3 = forms.CharField(
        required=False,
        label="Неисправность 3",
    )
    result = forms.CharField(
        label="Заключение",
        help_text=(
            "<i>Требует ремонта производителя,</i> <br>"
            "<i>требует регулировки/настройки, <br>не подлежит востановлению</i>"
        ),
    )

    class Meta:
        model = Defect_statement
        fields = ("defect_1", "defect_2", "defect_3", "result")