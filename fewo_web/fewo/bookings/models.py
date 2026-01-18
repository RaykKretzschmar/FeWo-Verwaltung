from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from properties.models import Property
from customers.models import Customer

class Booking(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Entwurf')
        CONFIRMED = 'confirmed', _('Bestätigt')
        CANCELED = 'canceled', _('Storniert')

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Ferienwohnung"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Kunde"))
    check_in = models.DateField(verbose_name=_("Check-in"))
    check_out = models.DateField(verbose_name=_("Check-out"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name=_("Status"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Gesamtpreis"))
    notes = models.TextField(blank=True, verbose_name=_("Notizen"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError({
                'check_out': _('Das Check-out-Datum muss nach dem Check-in-Datum liegen.')
            })

    def __str__(self):
        return f"{self.property.name} - {self.customer} ({self.check_in} bis {self.check_out})"

    class Meta:
        verbose_name = _("Buchung")
        verbose_name_plural = _("Buchungen")
        ordering = ['-check_in']
