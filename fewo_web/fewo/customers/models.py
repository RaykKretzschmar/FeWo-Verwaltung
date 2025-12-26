from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    PRIVATE = "Privat"
    COMPANY = "Firma"
    CUSTOMER_TYPE_CHOICES = [
        (PRIVATE, "Privat"),
        (COMPANY, "Firma"),
    ]

    customer_type = models.CharField(
        max_length=10, choices=CUSTOMER_TYPE_CHOICES, default=PRIVATE, verbose_name="Kundentyp"
    )
    salutation = models.CharField(max_length=20, blank=True, verbose_name="Anrede")
    first_name = models.CharField(max_length=50, verbose_name="Vorname")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Nachname")
    company_name = models.CharField(max_length=100, blank=True, verbose_name="Firmenname")
    city = models.CharField(max_length=50, verbose_name="Stadt")
    postal_code = models.CharField(max_length=10, verbose_name="PLZ")
    street = models.CharField(max_length=50, verbose_name="Straße")
    house_number = models.CharField(max_length=10, verbose_name="Hausnummer")
    customer_number = models.CharField(max_length=20, unique=True, default="", verbose_name="Kundennummer")

    def save(self, *args, **kwargs):
        if not self.customer_number:
            self.customer_number = timezone.now().strftime("%Y%m%d%H%M%S")
        super().save(*args, **kwargs)

    def __str__(self):
        if self.customer_type == self.COMPANY:
            return self.company_name or f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
