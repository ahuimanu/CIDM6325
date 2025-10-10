#!/usr/bin/env python
"""
Test script to verify Django setup and create sample blog data
"""
import os
import sys
import django
from pathlib import Path

# Add the blog_project directory to Python path
blog_project_dir = Path(__file__).resolve().parent / "blog_project"
sys.path.insert(0, str(blog_project_dir.parent))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User
from blog_project.myblog.models import Post, Comment

def create_sample_data():
    """Create sample blog posts and users"""
    
    # Create users
    if not User.objects.filter(username='author1').exists():
        author1 = User.objects.create_user(
            username='author1',
            email='author1@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        print("✓ Created user: author1")
    else:
        author1 = User.objects.get(username='author1')
        print("✓ User author1 already exists")

    if not User.objects.filter(username='author2').exists():
        author2 = User.objects.create_user(
            username='author2',
            email='author2@example.com',
            password='password123',
            first_name='Jane',
            last_name='Smith'
        )
        print("✓ Created user: author2")
    else:
        author2 = User.objects.get(username='author2')
        print("✓ User author2 already exists")

    # Create sample posts
    posts_data = [
        {
            'title': 'Welcome to Our Blog',
            'slug': 'welcome-to-our-blog',
            'content': '''Welcome to our amazing blog! This is our first post where we introduce ourselves and share what you can expect from this blog.

We'll be covering various topics including technology, web development, and interesting insights from our daily work. Stay tuned for more exciting content!

Feel free to explore the site and don't hesitate to leave comments on posts that interest you.''',
            'author': author1,
            'status': 'published'
        },
        {
            'title': 'Django Development Best Practices',
            'slug': 'django-development-best-practices',
            'content': '''Django is a powerful web framework that allows developers to build robust web applications quickly. In this post, we'll explore some best practices for Django development.

## Key Principles

1. **Follow the DRY principle** - Don't Repeat Yourself
2. **Use Django's built-in features** - Authentication, admin, ORM
3. **Write tests** - Ensure your code works as expected
4. **Follow Django conventions** - Use the framework as intended

## Project Structure

Organize your Django project with clear separation of concerns. Keep your apps focused and reusable.

Django's "batteries included" philosophy means you get a lot of functionality out of the box. Take advantage of it!''',
            'author': author2,
            'status': 'published'
        },
        {
            'title': 'Building Accessible Web Applications',
            'slug': 'building-accessible-web-applications',
            'content': '''Accessibility is not an afterthought—it should be a core consideration in all web development projects. In this post, we'll discuss why accessibility matters and how to implement it.

## Why Accessibility Matters

- **Inclusive design** benefits everyone
- **Legal compliance** is often required
- **Better UX** for all users
- **SEO benefits** from semantic markup

## Key Accessibility Principles

1. **Perceivable** - Information must be presentable to users in ways they can perceive
2. **Operable** - Interface components must be operable
3. **Understandable** - Information and UI operation must be understandable
4. **Robust** - Content must be robust enough for various assistive technologies

Remember: good accessibility often leads to better code overall!''',
            'author': author1,
            'status': 'published'
        },
        {
            'title': 'Draft Post - Coming Soon',
            'slug': 'draft-post-coming-soon',
            'content': '''This is a draft post that's still being worked on. It won't appear in the public blog listing until it's published.

Draft posts are useful for:
- Working on content over time
- Getting feedback before publishing
- Planning future content

Stay tuned for more great content!''',
            'author': author2,
            'status': 'draft'
        }
    ]

    for post_data in posts_data:
        if not Post.objects.filter(slug=post_data['slug']).exists():
            post = Post.objects.create(**post_data)
            print(f"✓ Created post: {post.title}")
            
            # Add a sample comment to published posts
            if post.status == 'published':
                Comment.objects.create(
                    post=post,
                    author=author1 if post.author == author2 else author2,
                    content=f"Great post! Thanks for sharing these insights about {post.title.lower()}."
                )
                print(f"  ✓ Added comment to: {post.title}")
        else:
            print(f"✓ Post already exists: {post_data['title']}")

def main():
    """Main function to run the test"""
    print("🚀 Django Blog Setup Test")
    print("=" * 50)
    
    try:
        # Test database connection
        print(f"📊 Database: {Post.objects.count()} posts, {User.objects.count()} users")
        
        # Create sample data
        print("\n📝 Creating sample data...")
        create_sample_data()
        
        # Final status
        print(f"\n✅ Setup complete!")
        print(f"   📊 Total posts: {Post.objects.count()}")
        print(f"   📖 Published posts: {Post.objects.filter(status='published').count()}")
        print(f"   👥 Total users: {User.objects.count()}")
        print(f"   💬 Total comments: {Comment.objects.count()}")
        
        print(f"\n🌐 To start the server, run:")
        print(f"   cd blog_project")
        print(f"   python manage.py runserver")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)