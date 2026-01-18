import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fewo.settings')
django.setup()

from customers.models import Customer
from properties.models import Property
from invoices.models import Invoice
from django.contrib.auth.models import User

def create_test_invoice():
    user = User.objects.first()
    customer = Customer.objects.first()
    prop = Property.objects.first()

    if not customer or not prop:
        print("Please ensure at least one Customer and one Property exist.")
        return

    # Create an invoice for next week
    arrival = date.today() + timedelta(days=7)
    departure = arrival + timedelta(days=5)
    
    invoice = Invoice.objects.create(
        user=user,
        customer=customer,
        date=date.today(),
        invoice_number=f"INV-{date.today().strftime('%Y%m%d')}-TEST",
        arrival_date=arrival,
        departure_date=departure,
        rental_property=prop,
        price_per_night=100.00,
        include_breakfast=False,
        tax_percent=7.00
    )
    print(f"Created Invoice: {invoice} for {customer} at {prop} ({arrival} to {departure})")

if __name__ == '__main__':
    create_test_invoice()
