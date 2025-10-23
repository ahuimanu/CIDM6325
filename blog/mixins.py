# blog/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin

class AuthorOrStaffRequiredMixin(UserPassesTestMixin):
    """
    Only allow the post's author or staff to modify objects.
    """
    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        return u.is_authenticated and (u.is_staff or obj.author_id == u.id)
