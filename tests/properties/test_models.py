from django.test import TestCase
from properties.models import Property
from django.contrib.auth.models import User
from decimal import Decimal

class PropertyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.property = Property.objects.create(
            user=self.user,
            name="Test Apartment",
            description="A nice place",
            price_per_night=Decimal("100.00"),
            default_breakfast_price=Decimal("15.00"),
            default_tax_percent=Decimal("19.00")
        )

    def test_property_creation(self):
        self.assertTrue(isinstance(self.property, Property))
        self.assertEqual(self.property.__str__(), "Test Apartment")
        self.assertEqual(self.property.price_per_night, Decimal("100.00"))

    def test_property_defaults(self):
        # Test defaults if not specified
        prop = Property.objects.create(
            user=self.user,
            name="Default Apartment",
            price_per_night=Decimal("50.00")
        )
        self.assertEqual(prop.default_breakfast_price, Decimal("10.00"))
        self.assertEqual(prop.default_tax_percent, Decimal("7.00"))
