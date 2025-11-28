from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company_name = models.CharField(max_length=100, blank=True, verbose_name="Firmenname")
    street = models.CharField(max_length=100, blank=True, verbose_name="Straße")
    house_number = models.CharField(max_length=10, blank=True, verbose_name="Hausnummer")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="PLZ")
    city = models.CharField(max_length=100, blank=True, verbose_name="Stadt")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="E-Mail")
    tax_number = models.CharField(max_length=50, blank=True, verbose_name="Steuernummer")
    bank_details = models.TextField(blank=True, verbose_name="Bankverbindung")
    has_subscription = models.BooleanField(default=False, verbose_name="Hat Abo")
    
    def __str__(self):
        return f"Profile for {self.user.username}"
