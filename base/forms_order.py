from django import forms
from .models import Order, Component, Unit_payment, Purpose_payment


class Create_request_form(forms.ModelForm):
    payer = forms.ChoiceField(
        label='Плательщик',
        choices=Order.CHOICE_COMPANY,
        required=False,
    )
    component = forms.ModelChoiceField(
        queryset=Component.objects.all(),
        label='Компонент',
        widget=forms.Select(
            attrs={
                'id':'id_component_create_order'
            }
        ),
    )
    note = forms.CharField(
        label='Ссылка',
        help_text='Укажите ссылку на компонент в магазине. <br> Поле необязательно для заполнения.',
        required=False
    )
    class Meta:
        model = Order
        fields = ("__all__")


class Invoice_number_form(forms.Form):
    TRK = 'ТРК'
    EIS = 'ЭИС'
    VTS = 'ВТС'
    COMPANY_CHOICE = (
        (TRK, 'ТРК'),
        (EIS, 'ЭИС'),
        (VTS, 'ВТС'),
    )
    number = forms.CharField(
        label="Номер счета",
        help_text='Укажите номер счета',
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "544012Z"}
        ),
    )
    document = forms.FileField(
        label='Файл',
        help_text='Подгрузить файл счета',
        required=False,
    )
    invoice_amount = forms.FloatField(
        label="Сумма счета",
        help_text="Укажите сумму счета",
        required=False,
        widget=forms.NumberInput(
            attrs={"placeholder": "65000.55"}
        ),
    )
    provider = forms.CharField(
        label='Поставщик',
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Элитан/ЭКО ПАУЭР/Чип и Дип"}
        ),
    )
    payer = forms.ChoiceField(
        choices=COMPANY_CHOICE,
        label='Плательщик',
        required=False
    )
    unit_order = forms.ModelChoiceField(
        queryset=Unit_payment.objects.all(),
        label='Подразделение',
        required=False,
    )
    purpose_order = forms.ModelChoiceField(
        queryset=Purpose_payment.objects.all(),
        label='Назначение платежа',
        required=False,
    )
    delivery_time = forms.CharField(
        label="Срок поставки",
        help_text='1 нед. / 2 нед. / 3 нед.',
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "1 нед. / 2 нед. / 3 нед."}
        ),
    )
    

class Confirmation_form(forms.Form):
    invoice_number = forms.CharField(
        label="Номер счета",
        help_text='Укажите номер счета',
        required=False,
    )


class Report_order_form(forms.Form):
    TRK = 'ТРК'
    EIS = 'ЭИС'
    VTS = 'ВТС'
    COMPANY_CHOICE = (
        (TRK, 'ТРК'),
        (EIS, 'ЭИС'),
        (VTS, 'ВТС'),
    )
    date_before = forms.DateField(
        label='Дата с',
        widget=forms.TextInput(
            attrs={"type": "date"}
        ),
    )
    date_after = forms.DateField(
        label='Дата до',
        widget=forms.TextInput(
            attrs={"type": "date"}
        ),
    )
    company = forms.ChoiceField(
        choices=COMPANY_CHOICE,
        label='Компания',
    )


class Create_unit_order_form(forms.ModelForm):
    class Meta:
        model = Unit_payment
        fields = '__all__'
    

class Create_purpose_order_form(forms.ModelForm):
    class Meta:
        model = Purpose_payment
        fields = '__all__'