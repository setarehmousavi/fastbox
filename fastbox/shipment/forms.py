from django import forms
from .models import Parcel

class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        # Exclude fields automatically set or calculated
        exclude = ('sender', 'tracking_code', 'estimated_price', 'estimated_days', 'status', 'created_at')
        widgets = {
            'receiver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_address': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_address': forms.TextInput(attrs={'class': 'form-control'}),
            'origin_province': forms.TextInput(attrs={'class': 'form-control'}),
            'origin_city': forms.TextInput(attrs={'class': 'form-control'}),
            'destination_province': forms.TextInput(attrs={'class': 'form-control'}),
            'destination_city': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_type': forms.Select(attrs={'class': 'form-select'}),
            'package_type': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'value': forms.NumberInput(attrs={'class': 'form-control'}),
            'need_package': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }
class ParcelStatusForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-select-sm'})
        }
