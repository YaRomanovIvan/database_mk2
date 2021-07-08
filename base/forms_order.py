from django import forms
from .models import Request


class Create_request_form(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("__all__")
