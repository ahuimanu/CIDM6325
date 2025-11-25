from __future__ import annotations

import os
import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ProfileUploadTests(TestCase):
    def setUp(self) -> None:
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="tstuser", password="password")

    def tearDown(self) -> None:
        # cleanup any created files in tmpdir whose names start with avatars/
        # Best-effort cleanup.
        tmp = tempfile.gettempdir()
        for root, _dirs, files in os.walk(tmp):
            for f in files:
                if "avatars" in root:
                    try:
                        os.remove(os.path.join(root, f))
                    except Exception:
                        pass

    def test_profile_created_and_avatar_upload_form(self):
        # Ensure profile exists
        self.assertTrue(hasattr(self.user, "profile"))
        # GET profile page requires login
        self.client.login(username="tstuser", password="password")
        res = self.client.get("/accounts/profile/")
        self.assertEqual(res.status_code, 200)
