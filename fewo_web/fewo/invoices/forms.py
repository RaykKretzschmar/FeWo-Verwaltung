from django import forms
from .models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "customer",
            "date",
            "invoice_number",
            "arrival_date",
            "departure_date",
            "rental_property",
            "price_per_night",
            "include_breakfast",
            "breakfast_price",
            "tax_percent",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "arrival_date": forms.DateInput(attrs={"type": "date"}),
            "departure_date": forms.DateInput(attrs={"type": "date"}),
        }
