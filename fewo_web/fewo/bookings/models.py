from django.db import models
from django.utils.translation import gettext_lazy as _
from properties.models import Property
from customers.models import Customer

class Booking(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Entwurf')
        CONFIRMED = 'confirmed', _('Bestätigt')
        CANCELED = 'canceled', _('Storniert')

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Ferienwohnung"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Kunde"))
    check_in = models.DateField(verbose_name=_("Check-in"))
    check_out = models.DateField(verbose_name=_("Check-out"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name=_("Status"))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Gesamtpreis"))
    notes = models.TextField(blank=True, verbose_name=_("Notizen"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property.name} - {self.customer} ({self.check_in} bis {self.check_out})"

    class Meta:
        verbose_name = _("Buchung")
        verbose_name_plural = _("Buchungen")
        ordering = ['-check_in']
