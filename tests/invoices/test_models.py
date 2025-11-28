from django.test import TestCase
from invoices.models import Invoice
from customers.models import Customer
from properties.models import Property
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta

class InvoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Max",
            last_name="Mustermann",
            city="Berlin",
            postal_code="10115",
            street="Musterstraße",
            house_number="1",
            customer_number="1234567891",
            customer_type="Privat"
        )
        self.property = Property.objects.create(
            user=self.user,
            name="Test Apartment",
            price_per_night=Decimal("100.00")
        )
        self.invoice = Invoice.objects.create(
            user=self.user,
            customer=self.customer,
            invoice_number="2023001",
            arrival_date=date.today(),
            departure_date=date.today() + timedelta(days=5),
            rental_property=self.property,
            price_per_night=Decimal("100.00"),
            include_breakfast=True,
            breakfast_price=Decimal("10.00"),
            tax_percent=Decimal("7.00")
        )

    def test_invoice_nights_calculation(self):
        self.assertEqual(self.invoice.nights, 5)

    def test_invoice_lodging_total(self):
        # 5 nights * 100.00 = 500.00
        self.assertEqual(self.invoice.lodging_total, Decimal("500.00"))

    def test_invoice_breakfast_total(self):
        # 5 nights * 10.00 = 50.00
        self.assertEqual(self.invoice.breakfast_total, Decimal("50.00"))

    def test_invoice_total_price(self):
        # 500.00 + 50.00 = 550.00
        self.assertEqual(self.invoice.total_price, Decimal("550.00"))

    def test_invoice_net_amount(self):
        # 550.00 / 1.07 = 514.02
        self.assertEqual(self.invoice.net_amount, Decimal("514.02"))

    def test_invoice_tax_amount(self):
        # 550.00 - 514.02 = 35.98
        self.assertEqual(self.invoice.tax_amount, Decimal("35.98"))

    def test_invoice_without_breakfast(self):
        self.invoice.include_breakfast = False
        self.invoice.save()
        self.assertEqual(self.invoice.breakfast_total, Decimal("0.00"))
        self.assertEqual(self.invoice.total_price, Decimal("500.00"))
