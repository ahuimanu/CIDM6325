from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.utils import timezone


class PostCBVTests(TestCase):
    """
    Test CRUD operations for Post CBVs.
    """

    def setUp(self) -> None:
        self.post = Post.objects.create(
            title="Test Post",
            body="Test body",
            publish_date=timezone.now(),
        )

    def test_post_list_view(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_post_detail_view(self):
        response = self.client.get(
            reverse("blog:post_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.body)

    def test_post_create_view(self):
        response = self.client.post(
            reverse("blog:post_create"),
            {
                "title": "New Post",
                "body": "New body",
                "publish_date": timezone.now(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="New Post").exists())

    def test_post_update_view(self):
        response = self.client.post(
            reverse("blog:post_update", kwargs={"slug": self.post.slug}),
            {
                "title": "Updated Title",
                "body": "Updated body",
                "publish_date": timezone.now(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_post_delete_view(self):
        response = self.client.post(
            reverse("blog:post_delete", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_detail_renders_markdown_safely(self):
        """
        The post detail view should render Markdown and sanitize HTML.
        """
        self.post.body = "**Bold** and [link](https://example.com)<script>alert(1)</script>"
        self.post.save()
        response = self.client.get(
            reverse("blog:post_detail", kwargs={"slug": self.post.slug})
        )
        self.assertContains(response, "<strong>Bold</strong>")
        self.assertContains(response, '<a href="https://example.com"')
        self.assertNotContains(response, "<script>")    
