from django.db import models
from django.utils import timezone


class Customer(models.Model):
    PRIVATE = "Privat"
    COMPANY = "Firma"
    CUSTOMER_TYPE_CHOICES = [
        (PRIVATE, "Privat"),
        (COMPANY, "Firma"),
    ]

    customer_type = models.CharField(
        max_length=10, choices=CUSTOMER_TYPE_CHOICES, default=PRIVATE
    )
    salutation = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=10)
    customer_number = models.CharField(max_length=20, unique=True, default="")

    def save(self, *args, **kwargs):
        if not self.customer_number:
            self.customer_number = timezone.now().strftime("%Y%m%d%H%M%S")
        super().save(*args, **kwargs)

    def __str__(self):
        if self.customer_type == self.COMPANY:
            return self.company_name or f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
