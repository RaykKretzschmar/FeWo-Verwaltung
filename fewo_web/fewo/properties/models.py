from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, verbose_name="Name der Ferienwohnung")
    description = models.TextField(blank=True, verbose_name="Beschreibung")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preis pro Nacht")
    
    # Default settings for this property
    default_breakfast_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=10.00, verbose_name="Standard Frühstückspreis"
    )
    default_tax_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=7.00, verbose_name="Standard MwSt. Satz"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ferienwohnung"
        verbose_name_plural = "Ferienwohnungen"
