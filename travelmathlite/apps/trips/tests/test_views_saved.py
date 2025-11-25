"""
Tests for saved calculations views.

Tests list and delete views with access control (INV-1).
"""

import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import SavedCalculation

User = get_user_model()


class SavedCalculationViewTests(TestCase):
    """Test saved calculation list and delete views."""

    def setUp(self):
        """Create test users and calculations."""
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")

        # Create calculations for user1
        self.calc1_user1 = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs=json.dumps({"origin": "LAX"}),
            outputs=json.dumps({"distance": 100}),
        )
        self.calc2_user1 = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="cost",
            inputs=json.dumps({"price": 50}),
            outputs=json.dumps({"cost": 50}),
        )

        # Create calculation for user2
        self.calc1_user2 = SavedCalculation.objects.create(
            user=self.user2,
            calculator_type="distance",
            inputs=json.dumps({"origin": "JFK"}),
            outputs=json.dumps({"distance": 200}),
        )

    def test_saved_list_requires_login(self):
        """Test that saved list view requires authentication."""
        url = reverse("trips:saved_list")
        response = self.client.get(url)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_saved_list_shows_only_user_calculations(self):
        """Test INV-1: Users only see their own calculations."""
        self.client.login(username="user1", password="testpass123")
        url = reverse("trips:saved_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/saved_list.html")

        # Should contain user1's calculations
        self.assertContains(response, "LAX")
        self.assertContains(response, "price")

        # Should NOT contain user2's calculations
        self.assertNotContains(response, "JFK")

    def test_saved_list_ordering_newest_first(self):
        """Test that saved list orders newest first."""
        self.client.login(username="user1", password="testpass123")
        url = reverse("trips:saved_list")
        response = self.client.get(url)

        calcs = response.context["calculations"]
        # calc2 was created after calc1, so should be first
        self.assertEqual(calcs[0].pk, self.calc2_user1.pk)
        self.assertEqual(calcs[1].pk, self.calc1_user1.pk)

    def test_saved_list_empty_for_new_user(self):
        """Test that new user sees empty list."""
        User.objects.create_user(username="user3", password="testpass123")
        self.client.login(username="user3", password="testpass123")
        url = reverse("trips:saved_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No saved calculations yet")

    def test_delete_requires_login(self):
        """Test that delete view requires authentication."""
        url = reverse("trips:saved_delete", kwargs={"pk": self.calc1_user1.pk})
        response = self.client.get(url)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_delete_shows_confirmation_page(self):
        """Test that delete shows confirmation page for owner."""
        self.client.login(username="user1", password="testpass123")
        url = reverse("trips:saved_delete", kwargs={"pk": self.calc1_user1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trips/saved_confirm_delete.html")
        self.assertContains(response, "Confirm Delete")
        self.assertContains(response, "LAX")

    def test_delete_owner_can_delete(self):
        """Test that owner can delete their own calculation."""
        self.client.login(username="user1", password="testpass123")
        url = reverse("trips:saved_delete", kwargs={"pk": self.calc1_user1.pk})

        # Confirm calculation exists
        self.assertTrue(SavedCalculation.objects.filter(pk=self.calc1_user1.pk).exists())

        # POST to delete
        response = self.client.post(url)

        # Should redirect to list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("trips:saved_list"))

        # Calculation should be deleted
        self.assertFalse(SavedCalculation.objects.filter(pk=self.calc1_user1.pk).exists())

    def test_delete_non_owner_gets_404(self):
        """Test INV-1: Non-owner cannot access delete view (404)."""
        self.client.login(username="user2", password="testpass123")
        url = reverse("trips:saved_delete", kwargs={"pk": self.calc1_user1.pk})

        # GET should return 404
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        # POST should also return 404
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

        # Calculation should still exist
        self.assertTrue(SavedCalculation.objects.filter(pk=self.calc1_user1.pk).exists())

    def test_delete_non_owner_cannot_delete_via_post(self):
        """Test that non-owner cannot delete via direct POST."""
        self.client.login(username="user2", password="testpass123")
        url = reverse("trips:saved_delete", kwargs={"pk": self.calc1_user1.pk})

        # Try to delete user1's calculation
        response = self.client.post(url)

        # Should get 404
        self.assertEqual(response.status_code, 404)

        # Calculation should still exist
        self.assertTrue(SavedCalculation.objects.filter(pk=self.calc1_user1.pk).exists())

    def test_saved_list_pagination(self):
        """Test that pagination works correctly."""
        # Create 15 calculations for user1 (exceeds paginate_by of 10)
        for i in range(15):
            SavedCalculation.objects.create(
                user=self.user1,
                calculator_type="distance",
                inputs=json.dumps({"index": i}),
                outputs=json.dumps({}),
            )

        self.client.login(username="user1", password="testpass123")
        url = reverse("trips:saved_list")
        response = self.client.get(url)

        # Due to pruning, user should have max 10 calculations
        # (the 15 new ones replaced the 2 original ones, then pruned to 10)
        calcs = response.context["calculations"]
        self.assertLessEqual(len(calcs), 10)

    def test_saved_list_context_object_name(self):
        """Test that context has correct object name."""
        self.client.login(username="user1", password="testpass123")
        url = reverse("trips:saved_list")
        response = self.client.get(url)

        self.assertIn("calculations", response.context)
        self.assertIsNotNone(response.context["calculations"])
