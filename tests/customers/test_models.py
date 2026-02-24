from django.test import TestCase
from customers.models import Customer
from django.contrib.auth.models import User
from django.utils import timezone

class CustomerModelTest(TestCase):
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
            customer_number="1234567890",
            customer_type="Privat"
        )

    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEqual(self.customer.__str__(), "Max Mustermann")

    def test_customer_number_generation(self):
        new_customer = Customer.objects.create(
            user=self.user,
            first_name="Test",
            last_name="Gen",
            city="Berlin",
            postal_code="10115",
            street="Teststr",
            house_number="1",
            customer_type="Privat"
        )
        self.assertTrue(new_customer.customer_number)
        # Check if it looks like a timestamp format YYYYMMDD...
        self.assertTrue(new_customer.customer_number.isdigit())
        self.assertTrue(len(new_customer.customer_number) >= 12)

    def test_company_customer_string_representation(self):
        company_customer = Customer.objects.create(
            user=self.user,
            company_name="Test GmbH",
            customer_type="Firma",
            city="Hamburg",
            postal_code="20095",
            street="Hafenstraße",
            house_number="10"
        )
        self.assertEqual(company_customer.__str__(), "Test GmbH")

    def test_familie_salutation_is_available(self):
        self.assertIn(
            (Customer.SALUTATION_FAMILIE, "Familie"),
            Customer.SALUTATION_CHOICES,
        )
