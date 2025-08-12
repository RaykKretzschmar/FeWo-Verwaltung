from django.db import models
from customers.models import Customer
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

TWOPLACES = Decimal("0.01")


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    invoice_number = models.CharField(max_length=20, unique=True)
    arrival_date = models.DateField()
    departure_date = models.DateField()
    apartment_name = models.CharField(max_length=100)

    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    include_breakfast = models.BooleanField(default=False)
    breakfast_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=Decimal("10.00")
    )  # default 10€
    tax_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("7.00")
    )  # default 7%

    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True)

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
