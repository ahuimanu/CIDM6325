from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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

        
    def test_post_createview(self):
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "New title",
                "body": "New text",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.objects.last().body, "New text")