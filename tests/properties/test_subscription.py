from django.test import TestCase, Client
from django.urls import reverse
from properties.models import Property
from django.contrib.auth.models import User
from accounts.models import UserProfile
from decimal import Decimal

class SubscriptionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password')

    def test_create_first_property_no_subscription(self):
        """User without subscription should be able to create first property"""
        response = self.client.post(reverse('property_create'), {
            'name': 'First Apartment',
            'description': 'Description',
            'price_per_night': '100.00',
            'default_breakfast_price': '10.00',
            'default_tax_percent': '7.00'
        })
        self.assertEqual(response.status_code, 302) # Redirects on success
        self.assertEqual(Property.objects.count(), 1)

    def test_create_second_property_no_subscription(self):
        """User without subscription should NOT be able to create second property"""
        # Create first property
        Property.objects.create(user=self.user, name="First", price_per_night=100)
        
        # Try to create second
        response = self.client.post(reverse('property_create'), {
            'name': 'Second Apartment',
            'description': 'Description',
            'price_per_night': '100.00',
            'default_breakfast_price': '10.00',
            'default_tax_percent': '7.00'
        })
        
        # Should redirect to property_list with error, not create new property
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Property.objects.count(), 1)
        
        # Check for error message
        response = self.client.get(reverse('property_list'))
        messages = list(response.context['messages'])
        self.assertTrue(any("Abo" in str(m) for m in messages))

    def test_create_second_property_with_subscription(self):
        """User WITH subscription should be able to create second property"""
        # Give subscription
        self.profile.has_subscription = True
        self.profile.save()
        
        # Create first property
        Property.objects.create(user=self.user, name="First", price_per_night=100)
        
        # Try to create second
        response = self.client.post(reverse('property_create'), {
            'name': 'Second Apartment',
            'description': 'Description',
            'price_per_night': '100.00',
            'default_breakfast_price': '10.00',
            'default_tax_percent': '7.00'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Property.objects.count(), 2)
