from django.test import TestCase
from .models import Post

# Create your tests here.
class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(text="This was created from a test")
    
    def test_model_content(self):
        self.assertEqual(self.post.text, "This was created from a test")
