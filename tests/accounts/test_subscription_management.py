from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile

class SubscriptionManagementTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = UserProfile.objects.create(user=self.user, has_subscription=True)
        self.client.login(username='testuser', password='password')

    def test_settings_page_shows_subscription_status(self):
        """Test that settings page shows correct status"""
        # Subscribed
        response = self.client.get(reverse('profile_settings'))
        self.assertContains(response, "Premium")
        self.assertContains(response, "Abo kündigen")
        
        # Not subscribed
        self.profile.has_subscription = False
        self.profile.save()
        response = self.client.get(reverse('profile_settings'))
        self.assertContains(response, "Kostenlos")
        self.assertContains(response, "Jetzt upgraden")

    def test_cancel_subscription(self):
        """Test canceling subscription"""
        self.assertTrue(self.user.profile.has_subscription)
        
        response = self.client.post(reverse('cancel_subscription'))
        
        # Should redirect to profile_settings
        self.assertRedirects(response, reverse('profile_settings'))
        
        # Check subscription status
        self.user.profile.refresh_from_db()
        self.assertFalse(self.user.profile.has_subscription)
        
        # Check success message
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("gekündigt" in str(m) for m in messages))
