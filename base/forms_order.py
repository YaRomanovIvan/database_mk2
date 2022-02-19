from tabnanny import verbose
from django import forms
from .models import Order


class Create_request_form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("__all__")


class Invoice_number_form(forms.Form):
    number = forms.CharField(
        label="Номер счета",
        help_text='Укажите номер счета',
        required=False,
    )
    delivery_time = forms.CharField(
        label="Срок поставки",
        required=False,
    )