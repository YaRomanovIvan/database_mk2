from tabnanny import verbose
from django import forms
from .models import Order, Component


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