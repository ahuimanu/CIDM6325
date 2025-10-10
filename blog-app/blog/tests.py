from django.test import TestCase
from django.contrib.auth import get_user_model

from .forms import PostForm
from .models import Post, Tag


User = get_user_model()


class PostFormTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="alice", password="password")

	def test_clean_title_min_length(self):
		form = PostForm(data={
			"title": "short",
			"body": "This is a body that is long enough.",
			"status": "draft",
			"tags_csv": "",
		})
		self.assertFalse(form.is_valid())
		self.assertIn("title", form.errors)

	def test_banned_word_in_title(self):
		form = PostForm(data={
			"title": "This is clickbait title",
			"body": "Valid body content that does not repeat title.",
			"status": "draft",
			"tags_csv": "",
		})
		self.assertFalse(form.is_valid())
		self.assertIn("title", form.errors)

	def test_body_not_repeating_title(self):
		title = "A descriptive title"
		form = PostForm(data={
			"title": title,
			"body": title + " and more",
			"status": "draft",
			"tags_csv": "",
		})
		self.assertFalse(form.is_valid())
		self.assertIn("body", form.errors)

	def test_save_creates_tags(self):
		form = PostForm(data={
			"title": "A valid title",
			"body": "A sufficiently long body for the post.",
			"status": "draft",
			"tags_csv": "django, web",
		})
		self.assertTrue(form.is_valid())
		post = form.save(author=self.user)
		self.assertIsInstance(post, Post)
		tag_names = set(t.name for t in post.tags.all())
		self.assertEqual(tag_names, {"django", "web"})


class PermissionTests(TestCase):
	def setUp(self):
		self.author = User.objects.create_user(username="author", password="pw")
		self.other = User.objects.create_user(username="other", password="pw")
		self.post = Post.objects.create(title="Title for perms", body="body body body body body", author=self.author, status=Post.Status.DRAFT)

	def test_author_can_edit(self):
		self.assertEqual(self.post.author, self.author)

	def test_non_author_cannot_publish_without_permission(self):
		# other user should not have can_publish by default
		self.assertFalse(self.other.has_perm("blog.can_publish"))


class AuthFlowTests(TestCase):
	def test_register_and_login(self):
		resp = self.client.get("/accounts/register/")
		self.assertEqual(resp.status_code, 200)
		# register a new user
		resp = self.client.post("/accounts/register/", {"username": "bob", "password1": "complexpass123", "password2": "complexpass123"}, follow=True)
		self.assertEqual(resp.status_code, 200)
		# after registration the user should be authenticated
		user = resp.context.get("user")
		self.assertTrue(user.is_authenticated)


class ReviewWorkflowTests(TestCase):
	def setUp(self):
		self.reviewer = User.objects.create_user(username="rev", password="pw")
		self.publisher = User.objects.create_user(username="pub", password="pw")
		# give reviewer can_review permission and publisher can_publish permission
		from django.contrib.auth.models import Permission
		from django.contrib.contenttypes.models import ContentType
		from .models import Post

		ct = ContentType.objects.get_for_model(Post)
		can_review = Permission.objects.get(content_type=ct, codename="can_review")
		can_publish = Permission.objects.get(content_type=ct, codename="can_publish")
		self.reviewer.user_permissions.add(can_review)
		self.publisher.user_permissions.add(can_publish)
		# give publisher review permission so they can view review_list in tests
		self.publisher.user_permissions.add(can_review)

		# create a post in review
		self.post = Post.objects.create(title="Review me please", body="long body text here", author=self.publisher, status=Post.Status.REVIEW)

	def test_reviewer_sees_review_list(self):
		self.client.login(username="rev", password="pw")
		resp = self.client.get("/posts/review/")
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, "Review me please")

	def test_publish_action_requires_permission(self):
		# reviewer cannot publish unless they also have can_publish
		self.client.login(username="rev", password="pw")
		resp = self.client.post("/posts/review/", {"post_id": self.post.pk, "action": "publish"}, follow=True)
		self.assertContains(resp, "do not have permission")

	def test_publisher_can_publish_via_review(self):
		self.client.login(username="pub", password="pw")
		resp = self.client.post("/posts/review/", {"post_id": self.post.pk, "action": "publish"}, follow=True)
		self.post.refresh_from_db()
		self.assertEqual(self.post.status, Post.Status.PUBLISHED)

	def test_login_page_and_post(self):
		# create a user
		u = User.objects.create_user(username="carl", password="pw12345")
		resp = self.client.get("/accounts/login/")
		self.assertEqual(resp.status_code, 200)
		resp = self.client.post("/accounts/login/", {"username": "carl", "password": "pw12345"}, follow=True)
		self.assertEqual(resp.status_code, 200)
		user = resp.context.get("user")
		self.assertTrue(user.is_authenticated)

	def test_hx_search_returns_fragment(self):
		# create posts to search
		u = User.objects.create_user(username="searcher", password="pw")
		Post.objects.create(title="FindMe Please", body="body text", author=u, status=Post.Status.PUBLISHED)
		resp = self.client.get('/hx/search/?q=FindMe')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('FindMe Please', resp.content.decode())

	def test_hx_inline_edit_get_and_post(self):
		# create a user and a post
		user = User.objects.create_user(username="inline", password="pw")
		post = Post.objects.create(title="Inline Title", body="long body here", author=user, status=Post.Status.DRAFT)
		# login as author
		self.client.login(username="inline", password="pw")
		# GET should return the inline form fragment
		resp = self.client.get(f'/hx/posts/{post.pk}/inline/')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('form', resp.content.decode().lower())
		# POST an edit
		resp = self.client.post(f'/hx/posts/{post.pk}/inline/', {'title': 'Inline Title Edited', 'body': post.body, 'status': post.status, 'tags_csv': ''})
		self.assertEqual(resp.status_code, 200)
		post.refresh_from_db()
		self.assertEqual(post.title, 'Inline Title Edited')

