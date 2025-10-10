from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            author=self.user,
            content='This is a test post content.',
            status='published'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(post.status, 'published')
        
    def test_post_absolute_url(self):
        post = Post.objects.create(
            title='Test Post',
            author=self.user,
            content='Test content',
            status='published'
        )
        self.assertEqual(post.get_absolute_url(), '/post/test-post/')


class PostListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.published_post = Post.objects.create(
            title='Published Post',
            author=self.user,
            content='Published content',
            status='published'
        )
        self.draft_post = Post.objects.create(
            title='Draft Post',
            author=self.user,
            content='Draft content',
            status='draft'
        )
        
    def test_post_list_view(self):
        response = self.client.get(reverse('myblog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published Post')
        self.assertNotContains(response, 'Draft Post')
        
    def test_post_list_pagination(self):
        # Create multiple posts to test pagination
        for i in range(15):
            Post.objects.create(
                title=f'Post {i}',
                author=self.user,
                content=f'Content {i}',
                status='published'
            )
        response = self.client.get(reverse('myblog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            author=self.user,
            content='Test content',
            status='published'
        )
        
    def test_post_detail_view(self):
        response = self.client.get(
            reverse('myblog:post_detail', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        
    def test_post_detail_404_for_draft(self):
        draft_post = Post.objects.create(
            title='Draft Post',
            author=self.user,
            content='Draft content',
            status='draft'
        )
        response = self.client.get(
            reverse('myblog:post_detail', kwargs={'slug': draft_post.slug})
        )
        self.assertEqual(response.status_code, 404)
