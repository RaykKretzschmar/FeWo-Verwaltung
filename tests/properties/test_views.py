from django.test import TestCase, Client
from django.urls import reverse
from properties.models import Property
from django.contrib.auth.models import User
from decimal import Decimal
import json

from accounts.models import UserProfile

class PropertyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user, has_subscription=True)
        self.client.login(username='testuser', password='password')
        self.property = Property.objects.create(
            user=self.user,
            name="Test Apartment",
            price_per_night=Decimal("100.00")
        )

    def test_property_list_view(self):
        response = self.client.get(reverse('property_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Apartment")
        self.assertTemplateUsed(response, 'properties/property_list.html')

    def test_property_create_view(self):
        response = self.client.post(reverse('property_create'), {
            'name': 'New Apartment',
            'description': 'Brand new',
            'price_per_night': '150.00',
            'default_breakfast_price': '12.00',
            'default_tax_percent': '7.00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Property.objects.count(), 2)

    def test_property_update_view(self):
        response = self.client.post(reverse('property_update', args=[self.property.pk]), {
            'name': 'Updated Apartment',
            'description': 'Updated description',
            'price_per_night': '110.00',
            'default_breakfast_price': '10.00',
            'default_tax_percent': '7.00'
        })
        self.assertEqual(response.status_code, 302)
        self.property.refresh_from_db()
        self.assertEqual(self.property.name, 'Updated Apartment')
        self.assertEqual(self.property.price_per_night, Decimal("110.00"))

    def test_property_delete_view(self):
        response = self.client.post(reverse('property_delete', args=[self.property.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Property.objects.count(), 0)

    def test_get_property_details(self):
        response = self.client.get(reverse('property_details', args=[self.property.pk]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['price_per_night'], "100.00")
