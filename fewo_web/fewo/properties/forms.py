from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "name",
            "description",
            "price_per_night",
            "default_breakfast_price",
            "default_tax_percent",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price_per_night": forms.NumberInput(attrs={"class": "form-control"}),
            "default_breakfast_price": forms.NumberInput(attrs={"class": "form-control"}),
            "default_tax_percent": forms.NumberInput(attrs={"class": "form-control"}),
        }
