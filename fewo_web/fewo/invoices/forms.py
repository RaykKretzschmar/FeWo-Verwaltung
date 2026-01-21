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

    def clean(self):
        cleaned_data = super().clean()
        price_per_night = cleaned_data.get("price_per_night")
        arrival_date = cleaned_data.get("arrival_date")
        departure_date = cleaned_data.get("departure_date")
        rental_property = cleaned_data.get("rental_property")
        instance_id = self.instance.id if self.instance else None

        # P-01: Block negative prices
        if price_per_night is not None and price_per_night < 0:
            self.add_error("price_per_night", "Der Preis pro Nacht darf nicht negativ sein.")

        # Date and Availability Logic
        if arrival_date and departure_date:
            # P-02: Ensure Departure > Arrival
            if departure_date <= arrival_date:
                self.add_error("departure_date", "Das Abreisedatum muss nach dem Anreisedatum liegen.")
            
            # P-03: Check for Overlapping Bookings (Availability)
            elif rental_property:
                overlapping = Invoice.objects.filter(
                    rental_property=rental_property,
                    arrival_date__lt=departure_date,
                    departure_date__gt=arrival_date
                )
                
                if instance_id:
                    overlapping = overlapping.exclude(id=instance_id)

                if overlapping.exists():
                    self.add_error("rental_property", "Die Ferienwohnung ist in diesem Zeitraum bereits belegt.")
        
        return cleaned_data
