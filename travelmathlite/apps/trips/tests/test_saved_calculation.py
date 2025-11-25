"""
Tests for SavedCalculation model.

Tests model creation, JSON serialization, and pruning behavior (INV-2).
"""

import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.trips.models import SavedCalculation

User = get_user_model()


class SavedCalculationModelTests(TestCase):
    """Test SavedCalculation model functionality."""

    def setUp(self):
        """Create test users."""
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")

    def test_create_saved_calculation(self):
        """Test creating a SavedCalculation instance."""
        calc = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs=json.dumps({"origin": "LAX", "destination": "JFK"}),
            outputs=json.dumps({"distance": 2475, "unit": "miles"}),
        )

        self.assertEqual(calc.user, self.user1)
        self.assertEqual(calc.calculator_type, "distance")
        self.assertIsNotNone(calc.created_at)

    def test_get_inputs_method(self):
        """Test get_inputs returns dict."""
        calc = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs=json.dumps({"origin": "LAX", "destination": "JFK"}),
            outputs=json.dumps({}),
        )

        inputs = calc.get_inputs()
        self.assertIsInstance(inputs, dict)
        self.assertEqual(inputs["origin"], "LAX")
        self.assertEqual(inputs["destination"], "JFK")

    def test_get_outputs_method(self):
        """Test get_outputs returns dict."""
        calc = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs=json.dumps({}),
            outputs=json.dumps({"distance": 2475, "unit": "miles"}),
        )

        outputs = calc.get_outputs()
        self.assertIsInstance(outputs, dict)
        self.assertEqual(outputs["distance"], 2475)
        self.assertEqual(outputs["unit"], "miles")

    def test_set_inputs_method(self):
        """Test set_inputs stores dict as JSON."""
        calc = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs="{}",
            outputs="{}",
        )

        calc.set_inputs({"origin": "LAX", "destination": "JFK"})
        calc.save()

        # Reload from DB
        calc.refresh_from_db()
        inputs = calc.get_inputs()
        self.assertEqual(inputs["origin"], "LAX")

    def test_set_outputs_method(self):
        """Test set_outputs stores dict as JSON."""
        calc = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs="{}",
            outputs="{}",
        )

        calc.set_outputs({"distance": 2475, "unit": "miles"})
        calc.save()

        # Reload from DB
        calc.refresh_from_db()
        outputs = calc.get_outputs()
        self.assertEqual(outputs["distance"], 2475)

    def test_pruning_keeps_max_10_per_user(self):
        """
        Test INV-2: Creating 11th calculation prunes oldest for that user.

        Each user should have max 10 calculations. Creating an 11th should
        delete the oldest one automatically.
        """
        # Create 11 calculations for user1
        for i in range(11):
            SavedCalculation.objects.create(
                user=self.user1,
                calculator_type="distance",
                inputs=json.dumps({"index": i}),
                outputs=json.dumps({"result": i}),
            )

        # Should only have 10 entries for user1
        user1_calcs = SavedCalculation.objects.filter(user=self.user1)
        self.assertEqual(user1_calcs.count(), 10)

        # The oldest (index 0) should be gone
        indices = [calc.get_inputs()["index"] for calc in user1_calcs]
        self.assertNotIn(0, indices)
        self.assertIn(10, indices)

    def test_pruning_per_user_independent(self):
        """
        Test that pruning is per-user (one user's limit doesn't affect another).
        """
        # Create 11 for user1
        for i in range(11):
            SavedCalculation.objects.create(
                user=self.user1,
                calculator_type="distance",
                inputs=json.dumps({"index": i}),
                outputs=json.dumps({}),
            )

        # Create 5 for user2
        for i in range(5):
            SavedCalculation.objects.create(
                user=self.user2,
                calculator_type="cost",
                inputs=json.dumps({"index": i}),
                outputs=json.dumps({}),
            )

        # User1 should have 10, user2 should have 5
        self.assertEqual(SavedCalculation.objects.filter(user=self.user1).count(), 10)
        self.assertEqual(SavedCalculation.objects.filter(user=self.user2).count(), 5)

    def test_string_representation(self):
        """Test __str__ method."""
        calc = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs="{}",
            outputs="{}",
        )

        str_repr = str(calc)
        self.assertIn("user1", str_repr)
        self.assertIn("distance", str_repr)

    def test_ordering_newest_first(self):
        """Test that calculations are ordered newest first by default."""
        SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs=json.dumps({"index": 1}),
            outputs=json.dumps({}),
        )
        SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs=json.dumps({"index": 2}),
            outputs=json.dumps({}),
        )

        calcs = list(SavedCalculation.objects.filter(user=self.user1))
        self.assertEqual(calcs[0].get_inputs()["index"], 2)
        self.assertEqual(calcs[1].get_inputs()["index"], 1)

    def test_get_inputs_handles_invalid_json(self):
        """Test get_inputs returns empty dict for invalid JSON."""
        calc = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs="invalid json",
            outputs="{}",
        )

        inputs = calc.get_inputs()
        self.assertEqual(inputs, {})

    def test_get_outputs_handles_invalid_json(self):
        """Test get_outputs returns empty dict for invalid JSON."""
        calc = SavedCalculation.objects.create(
            user=self.user1,
            calculator_type="distance",
            inputs="{}",
            outputs="invalid json",
        )

        outputs = calc.get_outputs()
        self.assertEqual(outputs, {})
