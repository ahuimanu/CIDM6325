from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Post

# Create your tests here.

class PostModelTests(TestCase):
    """Test cases for the Post model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            content='This is a test post content.'
        )
    
    def test_post_creation(self):
        """Test that a post is created correctly"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.content, 'This is a test post content.')
        self.assertIsNotNone(self.post.date_created)
        self.assertIsNotNone(self.post.date_updated)
    
    def test_post_str_method(self):
        """Test the __str__ method returns the title"""
        self.assertEqual(str(self.post), 'Test Post')
    
    def test_post_get_absolute_url(self):
        """Test the get_absolute_url method"""
        expected_url = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)
    
    def test_post_ordering(self):
        """Test that posts are ordered by date_created descending"""
        # Small delay to ensure different timestamps
        import time
        time.sleep(0.01)
        
        # Create a second post
        post2 = Post.objects.create(
            title='Second Post',
            author=self.user,
            content='Second post content.'
        )
        
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)  # Most recent first
        self.assertEqual(posts[1], self.post)
    
    def test_date_updated_changes(self):
        """Test that date_updated changes when post is modified"""
        original_updated = self.post.date_updated
        
        # Small delay to ensure different timestamp
        import time
        time.sleep(0.01)
        
        self.post.title = 'Updated Test Post'
        self.post.save()
        
        self.assertNotEqual(self.post.date_updated, original_updated)


class BlogPostDetailViewTests(TestCase):
    """Test cases for the BlogPostDetailView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            content='This is a test post content.'
        )
    
    def test_post_detail_view_success(self):
        """Test that the post detail view returns 200 for valid post"""
        url = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        self.assertContains(response, self.post.author.username)
    
    def test_post_detail_view_404(self):
        """Test that the view returns 404 for non-existent post"""
        url = reverse('blog:post_detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_post_detail_view_context(self):
        """Test that the view provides correct context"""
        url = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.context['post'], self.post)
    
    def test_post_detail_view_template(self):
        """Test that the view uses the correct template"""
        url = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        
        self.assertTemplateUsed(response, 'blog/blog_view.html')
    
    def test_post_detail_view_displays_dates(self):
        """Test that the view displays creation and update dates"""
        url = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        
        # Check that dates are displayed in some format
        self.assertContains(response, 'Published:')
        # The exact date format will depend on Django's date filter
    
    def test_multiple_posts_individual_access(self):
        """Test that each post can be accessed individually"""
        # Create a second post
        post2 = Post.objects.create(
            title='Second Post',
            author=self.user,
            content='Second post content.'
        )
        
        # Test first post
        url1 = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
        response1 = self.client.get(url1)
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, 'Test Post')
        self.assertNotContains(response1, 'Second Post')
        
        # Test second post
        url2 = reverse('blog:post_detail', kwargs={'pk': post2.pk})
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Second Post')
        self.assertNotContains(response2, 'Test Post')
