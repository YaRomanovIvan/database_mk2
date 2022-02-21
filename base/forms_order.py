from tabnanny import verbose
from django import forms
from .models import Order, Component


class Create_request_form(forms.ModelForm):
    trk = "ТРК"
    vts = "ВТС"
    eis = "ЭИС"
    default = "--------"
    CHOICE_COMPANY = [
        (default, "--------"),
        (trk, "ТРК"),
        (vts, "ВТС"),
        (eis, "ЭИС"),
    ]
    payer = forms.ChoiceField(
        choices=CHOICE_COMPANY,
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
    )
    invoice_amount = forms.FloatField(
        label="Сумма счета",
        help_text="Укажите сумму счета",
        required=False,
    )
    provider = forms.CharField(
        label='Поставщик',
        required=False
    )
    payer = forms.ChoiceField(
        choices=COMPANY_CHOICE,
        label='Плательщик',
        required=False
    )
    delivery_time = forms.CharField(
        label="Срок поставки",
        required=False,
    )
    