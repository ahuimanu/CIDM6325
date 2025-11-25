"""
Signal handlers for the accounts app.

Handles user authentication events like login to migrate anonymous session data.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import receiver as _receiver

from core.session import mark_session_as_user_bound  # type: ignore[reportMissingImports]

from .models import Profile


@receiver(user_logged_in)
def migrate_anonymous_calculator_inputs(sender, request, user, **kwargs):  # type: ignore[no-untyped-def]
    """
    Migrate anonymous calculator inputs after user login.

    When a user logs in, we mark their session as user-bound so that any
    calculator inputs stored during anonymous browsing are now associated
    with their account. The next calculator submission will save to SavedCalculation.

    This does NOT create SavedCalculation records immediately - it only marks
    the session as ready for user-associated saves.

    Args:
        sender: The User model class
        request: HttpRequest with session
        user: The authenticated User instance
        **kwargs: Additional signal arguments
    """
    if request is None:
        return

    # Mark session as belonging to authenticated user
    mark_session_as_user_bound(request)

    # Note: We intentionally do NOT create SavedCalculation records here.
    # The calculator views will handle saving when the user actually submits
    # a new calculation after login.


# Auto-create Profile when a User is created
@_receiver(post_save, sender=get_user_model())
def create_profile_for_new_user(sender, instance, created, **kwargs):  # type: ignore[no-untyped-def]
    if created:
        try:
            Profile.objects.create(user=instance)
        except Exception:
            # Best-effort creation; avoid breaking user creation flow
            pass
