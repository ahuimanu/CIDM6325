from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Post

# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )

        cls.post = Post.objects.create(
            title="Test post",
            body="Test body content",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "Test post")
        self.assertEqual(self.post.body, "Test body content")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "Test post")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")