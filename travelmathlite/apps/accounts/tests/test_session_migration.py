"""
Tests for session migration signal handler.

Tests that user_logged_in signal correctly marks session as user-bound.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.test import RequestFactory, TestCase

from core.session import (
    is_session_user_bound,
    mark_session_as_user_bound,
    set_calculator_inputs,
)

User = get_user_model()


class SessionMigrationSignalTests(TestCase):
    """Test session migration on user login."""

    def setUp(self):
        """Set up test user and request factory."""
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.factory = RequestFactory()

    def test_mark_session_as_user_bound(self):
        """Test marking session as user-bound."""
        # Create a request with session
        request = self.factory.get("/")
        # Add session manually (normally added by middleware)
        from django.contrib.sessions.backends.db import SessionStore

        request.session = SessionStore()

        # Initially not user-bound
        self.assertFalse(is_session_user_bound(request))

        # Mark as user-bound
        mark_session_as_user_bound(request)

        # Now should be user-bound
        self.assertTrue(is_session_user_bound(request))

    def test_session_migration_signal_marks_user_bound(self):
        """Test that user_logged_in signal marks session as user-bound."""
        # Create a request with session
        request = self.factory.get("/")
        from django.contrib.sessions.backends.db import SessionStore

        request.session = SessionStore()

        # Add some calculator inputs to session
        set_calculator_inputs(request, "distance", {"origin": "LAX", "destination": "JFK"})

        # Initially not user-bound
        self.assertFalse(is_session_user_bound(request))

        # Trigger the signal (simulating login)
        user_logged_in.send(sender=User, request=request, user=self.user)

        # Session should now be marked as user-bound
        self.assertTrue(is_session_user_bound(request))

    def test_session_migration_safe_with_no_data(self):
        """Test that signal handler is safe when no session data present."""
        request = self.factory.get("/")
        from django.contrib.sessions.backends.db import SessionStore

        request.session = SessionStore()

        # Trigger signal with empty session - should not error
        user_logged_in.send(sender=User, request=request, user=self.user)

        # Should be marked as user-bound
        self.assertTrue(is_session_user_bound(request))

    def test_session_migration_idempotent(self):
        """Test that signal can be called multiple times safely."""
        request = self.factory.get("/")
        from django.contrib.sessions.backends.db import SessionStore

        request.session = SessionStore()

        # Call signal multiple times
        user_logged_in.send(sender=User, request=request, user=self.user)
        user_logged_in.send(sender=User, request=request, user=self.user)

        # Should still be user-bound (no errors)
        self.assertTrue(is_session_user_bound(request))

    def test_session_migration_no_request(self):
        """Test that signal handler handles None request gracefully."""
        # This should not raise an error
        try:
            user_logged_in.send(sender=User, request=None, user=self.user)
        except Exception as e:
            self.fail(f"Signal handler raised exception with None request: {e}")
