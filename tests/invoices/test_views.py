from django.test import TestCase, Client
from django.urls import reverse
from invoices.models import Invoice
from customers.models import Customer
from properties.models import Property
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
from unittest.mock import patch

class InvoiceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Max",
            last_name="Mustermann",
            city="Berlin",
            postal_code="10115",
            street="Musterstraße",
            house_number="1",
            customer_number="1234567892",
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

    def test_invoice_list_view(self):
        response = self.client.get(reverse('invoice_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2023001")
        self.assertTemplateUsed(response, 'invoices/invoice_list.html')

    @patch('invoices.views.generate_invoice_documents')
    def test_invoice_create_view(self, mock_generate):
        response = self.client.post(reverse('invoice_create'), {
            'customer': self.customer.pk,
            'rental_property': self.property.pk,
            'invoice_number': '2023002',
            'date': date.today(),
            'arrival_date': date.today(),
            'departure_date': date.today() + timedelta(days=3),
            'price_per_night': '120.00',
            'include_breakfast': 'on',
            'breakfast_price': '15.00',
            'tax_percent': '19.00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Invoice.objects.count(), 2)
        mock_generate.assert_called_once()

    def test_invoice_delete_view(self):
        response = self.client.post(reverse('invoice_delete', args=[self.invoice.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Invoice.objects.count(), 0)
