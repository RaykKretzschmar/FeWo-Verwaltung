from django.test import TestCase, Client
from django.urls import reverse
from customers.models import Customer
from django.contrib.auth.models import User

class CustomerViewTest(TestCase):
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
            customer_number="1234567893",
            customer_type="Privat"
        )

    def test_customer_list_view(self):
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Max Mustermann")
        self.assertTemplateUsed(response, 'customers/customer_list.html')

    def test_customer_create_view(self):
        response = self.client.post(reverse('customer_create'), {
            'first_name': 'Erika',
            'last_name': 'Musterfrau',
            'city': 'München',
            'postal_code': '80331',
            'street': 'Marienplatz',
            'house_number': '1',
            'customer_type': 'Privat',
            'salutation': 'Frau'
        })
        self.assertEqual(response.status_code, 302) # Redirects after success
        self.assertEqual(Customer.objects.count(), 2)

    def test_customer_update_view(self):
        response = self.client.post(reverse('customer_update', args=[self.customer.pk]), {
            'first_name': 'Maximilian',
            'last_name': 'Mustermann',
            'city': 'Berlin',
            'postal_code': '10115',
            'street': 'Musterstraße',
            'house_number': '1',
            'customer_type': 'Privat',
            'salutation': 'Herr'
        })
        self.assertEqual(response.status_code, 302)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'Maximilian')

    def test_customer_create_view_with_familie_salutation(self):
        response = self.client.post(reverse('customer_create'), {
            'first_name': 'Anna',
            'last_name': 'Muster',
            'city': 'Leipzig',
            'postal_code': '04109',
            'street': 'Markt',
            'house_number': '2',
            'customer_type': 'Privat',
            'salutation': 'Familie'
        })
        self.assertEqual(response.status_code, 302)
        created_customer = Customer.objects.get(first_name='Anna', last_name='Muster')
        self.assertEqual(created_customer.salutation, 'Familie')

    def test_customer_delete_view(self):
        response = self.client.post(reverse('customer_delete', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 0)
