#!/usr/bin/env python
"""
Simple script to create sample blog posts for the Django blog.
Run this script to populate the database with some example content.
"""
import os
import sys
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

django.setup()

from django.contrib.auth.models import User
from myblog.models import Post, Comment

def create_sample_data():
    """Create sample blog posts and comments."""
    
    # Get or create the admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    # Set password for admin user
    admin_user.set_password('admin123')
    admin_user.save()
    
    # Create sample posts
    posts_data = [
        {
            'title': 'Welcome to MyBlog',
            'content': '''Welcome to our new blog! This is our first post, and we're excited to share our thoughts and insights with you.

This blog will cover a variety of topics including technology, web development, Django tips and tricks, and much more. 

We hope you find our content useful and engaging. Feel free to leave comments and share your thoughts!''',
            'status': 'published'
        },
        {
            'title': 'Getting Started with Django',
            'content': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

Here are some key features of Django:

1. **Rapid Development**: Django was designed to help developers take applications from concept to completion as quickly as possible.

2. **Security**: Django takes security seriously and helps developers avoid many common security mistakes.

3. **Scalable**: Some of the busiest sites on the Web leverage Django's ability to quickly and flexibly scale.

4. **Versatile**: Companies, organizations and governments have used Django to build all sorts of things — from content management systems to social networks to scientific computing platforms.

In future posts, we'll dive deeper into Django development techniques and best practices.''',
            'status': 'published'
        },
        {
            'title': 'The Importance of Web Accessibility',
            'content': '''Web accessibility means that websites, tools, and technologies are designed and developed so that people with disabilities can use them. More specifically, people can:

- Perceive, understand, navigate, and interact with the Web
- Contribute to the Web

Web accessibility encompasses all disabilities that affect access to the Web, including:
- Auditory
- Cognitive
- Neurological
- Physical
- Speech
- Visual

When websites and web tools are properly designed and coded, people with disabilities can use them. However, currently many sites and tools are developed with accessibility barriers that make them difficult or impossible for some people to use.

Making the web accessible benefits individuals, businesses, and society. International web standards define what is needed for accessibility.''',
            'status': 'published'
        },
        {
            'title': 'Coming Soon: Advanced Features',
            'content': '''We're working on some exciting new features for the blog! Here's a sneak peek of what's coming:

- **User Registration**: Soon readers will be able to create accounts and manage their profiles
- **Comment System**: Enhanced commenting with threaded replies
- **Categories and Tags**: Better organization of content
- **Search Functionality**: Find exactly what you're looking for
- **Social Sharing**: Easy sharing on social media platforms

Stay tuned for these updates. We're committed to making this the best blogging platform for our community!

This post is currently in draft status and will be published once these features are ready.''',
            'status': 'draft'
        }
    ]
    
    # Create posts
    created_posts = []
    for post_data in posts_data:
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'content': post_data['content'],
                'author': admin_user,
                'status': post_data['status']
            }
        )
        created_posts.append(post)
        if created:
            print(f"Created post: {post.title}")
        else:
            print(f"Post already exists: {post.title}")
    
    # Create some sample comments for the first two posts
    comments_data = [
        {
            'post': created_posts[0],
            'content': 'Great to see this blog getting started! Looking forward to more content.',
        },
        {
            'post': created_posts[0],
            'content': 'Welcome! This looks like it will be a valuable resource.',
        },
        {
            'post': created_posts[1],
            'content': 'Django is indeed a fantastic framework. Thanks for the overview!',
        },
        {
            'post': created_posts[1],
            'content': 'I\'ve been learning Django and this post is very helpful. Can\'t wait for the deep-dive posts!',
        },
        {
            'post': created_posts[2],
            'content': 'Accessibility is so important and often overlooked. Thank you for highlighting this topic.',
        }
    ]
    
    for comment_data in comments_data:
        comment, created = Comment.objects.get_or_create(
            post=comment_data['post'],
            content=comment_data['content'],
            defaults={'author': admin_user}
        )
        if created:
            print(f"Created comment on '{comment.post.title}'")
    
    print(f"\nSample data creation complete!")
    print(f"Created {Post.objects.filter(status='published').count()} published posts")
    print(f"Created {Post.objects.filter(status='draft').count()} draft posts")
    print(f"Created {Comment.objects.count()} comments")
    print(f"\nAdmin login details:")
    print(f"Username: admin")
    print(f"Password: admin123")
    print(f"Admin URL: http://127.0.0.1:8000/admin/")

if __name__ == '__main__':
    create_sample_data()