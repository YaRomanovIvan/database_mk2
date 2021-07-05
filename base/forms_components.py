from django import forms
from .models import Component

class New_component_form(forms.ModelForm):
    type_component = forms.CharField(
        label='Тип компонента',
        help_text = 'Например "стабилизатор"',
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm'
            }
        ),
    )
    marking = forms.CharField(
        label='Маркировка',
        help_text = 'Например "78L05"',
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm'
            }
        ),
    )
    note = forms.CharField(
        label='Примечание',
        required=False,
        help_text = 'Например "SOT-89"',
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm'
            }
        ),
    )
    price = forms.IntegerField(
        label='Цена за единицу',
        widget=forms.NumberInput(
            attrs={
                'class':'form-control form-control-sm'
            }
        ),
    )

    class Meta:
        model = Component
        fields = (
            'type_component',
            'marking',
            'note',
            'amount_eis',
            'amount_trk',
            'amount_vts',
            'price',
        )
        widgets = {
            'amount_eis': forms.NumberInput(
                attrs={
                    'class':'form-control form-control-sm'
                }
            ),
            'amount_trk': forms.NumberInput(
                attrs={
                    'class':'form-control form-control-sm'
                }
            ),
            'amount_vts': forms.NumberInput(
                attrs={
                    'class':'form-control form-control-sm'
                }
            ),
        }


class Update_amount_form(forms.Form):
    UNK = '---------'
    TRK = 'ТРК'
    EIS = 'ЭИС'
    VTS = 'ВТС'
    COMPANY_CHOICE = (
        (UNK, '---------'),
        (TRK, 'ТРК'),
        (EIS, 'ЭИС'),
        (VTS, 'ВТС'),
    )
    component = forms.ModelChoiceField(
        queryset=Component.objects.all(),
        label='Наименование компонента',
        widget=forms.Select(
            attrs={
                'id': 'id_update_component',
                'class':'form-control form-control-sm',
            }
        )
    )
    amount = forms.IntegerField(
        label='Количество',
        widget=forms.NumberInput(
            attrs={
                'id': 'id_update_amount',
                'class':'form-control form-control-sm',
            }
        )
    )
    company = forms.ChoiceField(
        choices=COMPANY_CHOICE,
        label='Компания',
        widget=forms.Select(
            attrs={
                'id': 'id_update_company',
                'class':'form-control form-control-sm',
            }
        )
    )         


class Update_price_form(forms.Form):
    component = forms.ModelChoiceField(
        queryset=Component.objects.all(),
        label='Наименование компонента',
        widget=forms.Select(
            attrs={
                'id': 'id_update_component_price',
                'class':'form-control form-control-sm',
            }
        )
    )
    price = forms.IntegerField(
        label='Цена за единицу',
        widget=forms.NumberInput(
            attrs={
                'id': 'id_update_price',
                'class':'form-control form-control-sm',
            }
        )
    )


class Edit_component_form(forms.ModelForm):
    note = forms.CharField(
        required=False,
    )
    class Meta:
        model = Component
        fields = (
            'id',
            'type_component',
            'marking',
            'note',
            'amount_eis',
            'amount_trk',
            'amount_vts',
            'price',
        )