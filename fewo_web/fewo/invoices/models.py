from django.db import models
from customers.models import Customer
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

TWOPLACES = Decimal("0.01")


from properties.models import Property
from django.contrib.auth.models import User

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Kunde")
    date = models.DateField(default=date.today, verbose_name="Rechnungsdatum")
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name="Rechnungsnummer")
    arrival_date = models.DateField(verbose_name="Anreisedatum")
    departure_date = models.DateField(verbose_name="Abreisedatum")
    rental_property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, verbose_name="Ferienwohnung")
    
    # Snapshot of prices at the time of invoice creation
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis pro Nacht")
    include_breakfast = models.BooleanField(default=False, verbose_name="Frühstück inklusive")
    breakfast_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal("10.00"), verbose_name="Preis für Frühstück"
    )
    tax_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("7.00"), verbose_name="Steuersatz (%)"
    )

    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True, verbose_name="PDF Datei")
    docx_file = models.FileField(upload_to="invoices/", blank=True, null=True, verbose_name="Word Datei")

    @property
    def nights(self) -> int:
        return max(0, (self.departure_date - self.arrival_date).days)

    @property
    def breakfast_total(self) -> Decimal:
        if not self.include_breakfast:
            return Decimal("0.00")
        return (Decimal(self.nights) * self.breakfast_price).quantize(
            TWOPLACES, rounding=ROUND_HALF_UP
        )

    @property
    def lodging_total(self) -> Decimal:
        return (Decimal(self.nights) * self.price_per_night).quantize(
            TWOPLACES, rounding=ROUND_HALF_UP
        )

    @property
    def total_price(self) -> Decimal:
        total = self.lodging_total + self.breakfast_total
        return total.quantize(TWOPLACES, rounding=ROUND_HALF_UP)

    @property
    def net_amount(self) -> Decimal:
        if self.tax_percent == 0:
            return self.total_price
        net = self.total_price * Decimal(100) / (Decimal(100) + self.tax_percent)
        return net.quantize(TWOPLACES, rounding=ROUND_HALF_UP)

    @property
    def tax_amount(self) -> Decimal:
        tax = (self.total_price - self.net_amount).quantize(
            TWOPLACES, rounding=ROUND_HALF_UP
        )
        return tax

    def __str__(self):
        return f"Invoice {self.invoice_number} — {self.customer}"
