from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile

class SubscriptionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        # Ensure profile exists (signal might create it, but explicit creation is safer for test isolation if signals aren't used)
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.client.login(username='testuser', password='password')

    def test_subscription_page_access(self):
        """Test accessing the subscription page"""
        response = self.client.get(reverse('subscription'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/subscription.html')

    def test_subscribe_action(self):
        """Test clicking the subscribe button"""
        self.assertFalse(self.user.profile.has_subscription)
        
        response = self.client.post(reverse('subscription'))
        
        # Should redirect to property_list
        self.assertRedirects(response, reverse('property_list'))
        
        # Check subscription status
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.has_subscription)
        
        # Check success message
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Glückwunsch" in str(m) for m in messages))

    def test_sidebar_link_visibility(self):
        """Test that the link is visible when not subscribed and hidden when subscribed"""
        # Not subscribed
        response = self.client.get(reverse('property_list'))
        self.assertContains(response, "Jetzt abonnieren")
        
        # Subscribe
        self.user.profile.has_subscription = True
        self.user.profile.save()
        
        # Subscribed
        response = self.client.get(reverse('property_list'))
        self.assertNotContains(response, "Jetzt abonnieren")
