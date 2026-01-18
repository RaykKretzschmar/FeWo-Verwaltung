from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from properties.models import Property
from invoices.models import Invoice
from customers.models import Customer


class BookingViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create a property for testing
        self.property = Property.objects.create(
            name='Test Property',
            user=self.user,
            price_per_night=100.00
        )
        
        # Create a customer for testing
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            user=self.user
        )
        
        # Create an invoice with dates for testing
        self.invoice = Invoice.objects.create(
            customer=self.customer,
            rental_property=self.property,
            user=self.user,
            arrival_date='2024-01-01',
            departure_date='2024-01-07',
            invoice_number='INV-2024-001',
            price_per_night=100.00
        )
    
    def test_calendar_view_with_invalid_property_id(self):
        """Test that calendar_view handles invalid property_id gracefully"""
        response = self.client.get(reverse('calendar_view') + '?property=invalid')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('property', response.context)
    
    def test_calendar_view_with_valid_property_id(self):
        """Test that calendar_view works with valid property_id"""
        response = self.client.get(reverse('calendar_view') + f'?property={self.property.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('property', response.context)
        self.assertEqual(response.context['property'], self.property)
    
    def test_booking_api_with_invalid_property_id(self):
        """Test that booking_api handles invalid property_id gracefully"""
        response = self.client.get(reverse('booking_api') + '?property=invalid')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Should return all invoices for the user since invalid property_id is ignored
        self.assertEqual(len(data), 1)
    
    def test_booking_api_with_valid_property_id(self):
        """Test that booking_api filters by valid property_id"""
        response = self.client.get(reverse('booking_api') + f'?property={self.property.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], self.invoice.id)
    
    def test_booking_api_without_property_id(self):
        """Test that booking_api works without property_id parameter"""
        response = self.client.get(reverse('booking_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
