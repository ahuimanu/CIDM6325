from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from .models import Post


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
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post.slug}))
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
        response = self.client.post(reverse("blog:post_delete", kwargs={"slug": self.post.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_detail_renders_markdown_safely(self):
        """
        The post detail view should render Markdown and sanitize HTML.
        """
        self.post.body = "**Bold** and [link](https://example.com)<script>alert(1)</script>"
        self.post.save()
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post.slug}))
        self.assertContains(response, "<strong>Bold</strong>")
        self.assertContains(response, '<a href="https://example.com"')
        self.assertNotContains(response, "<script>")

    def test_new_route_not_captured_by_slug(self):
        # Ensures ordering protects 'new' from the slug pattern
        resolver = resolve("/blog/post/new/")
        self.assertEqual(resolver.view_name, "blog:post_create")


class FeedsSitemapSeoTests(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title="SEO Post",
            body="Body text for SEO and feeds.",
            publish_date=timezone.now(),
        )

    def test_rss_feed_contains_post_link(self):
        url = reverse("blog:feed_rss")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.post.get_absolute_url(), resp.content.decode())

    def test_atom_feed_contains_post_link(self):
        url = reverse("blog:feed_atom")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.post.get_absolute_url(), resp.content.decode())

    def test_sitemap_includes_post(self):
        resp = self.client.get("/sitemap.xml")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.post.get_absolute_url(), resp.content.decode())

    def test_canonical_tag_on_detail(self):
        detail = reverse("blog:post_detail", kwargs={"slug": self.post.slug})
        resp = self.client.get(detail)
        self.assertEqual(resp.status_code, 200)
        expected_canonical = f"http://testserver{self.post.get_absolute_url()}"
        self.assertIn(
            f'<link rel="canonical" href="{expected_canonical}"',
            resp.content.decode(),
        )


class RootIndexTests(TestCase):
    def test_root_redirects_to_blog(self):
        resp = self.client.get("/")
        # non-permanent redirect
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers.get("Location"), reverse("blog:post_list"))


class SearchTests(TestCase):
    def setUp(self) -> None:
        now = timezone.now()
        for i in range(25):
            Post.objects.create(
                title=f"Alpha {i}",
                body=("Body with term foo." if i % 2 == 0 else "Irrelevant text"),
                publish_date=now,
            )

    def test_search_happy_path(self):
        resp = self.client.get(reverse("blog:post_search"), {"q": "foo"})
        self.assertEqual(resp.status_code, 200)
        # Should find posts where body contains 'foo'
        self.assertContains(resp, "foo", html=False)
        self.assertIn("count", resp.context)
        self.assertGreater(resp.context["count"], 0)

    def test_empty_query_shows_zero_state(self):
        resp = self.client.get(reverse("blog:post_search"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Type a term above", html=False)

    def test_pagination_and_query_preserved(self):
        # With page size 10, ensure next page link carries q
        resp = self.client.get(reverse("blog:post_search"), {"q": "Alpha", "page": 1})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "?q=Alpha&amp;page=2")

    def test_html_escaping_in_snippet(self):
        # Create a post with HTML in body and search for a term within it
        Post.objects.create(title="XSS Test", body="<b>danger</b>", publish_date=timezone.now())
        resp = self.client.get(reverse("blog:post_search"), {"q": "danger"})
        self.assertEqual(resp.status_code, 200)
        # Ensure bold tag is escaped in snippet (not rendered as HTML) and match is highlighted
        self.assertContains(
            resp,
            '&lt;b&gt;<mark class="highlight">danger</mark>&lt;/b&gt;',
            html=False,
        )
