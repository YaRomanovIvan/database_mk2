from django import forms
from .models import Order


class Create_request_form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("__all__")
