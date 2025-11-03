from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import Post


class Command(BaseCommand):
    help = "Create common groups and assign permissions for the blog (editor, publisher)."

    def handle(self, *args, **options):
        # Ensure content type exists for Post
        ct = ContentType.objects.get_for_model(Post)

        # Standard model permissions
        change_perm = Permission.objects.get(content_type=ct, codename="change_post")
        delete_perm = Permission.objects.get(content_type=ct, codename="delete_post")

        # Custom perms defined in Post.Meta
        can_review = Permission.objects.get(content_type=ct, codename="can_review")
        can_publish = Permission.objects.get(content_type=ct, codename="can_publish")

        # Editor group: can review and change posts
        editor, created = Group.objects.get_or_create(name="editor")
        editor.permissions.add(change_perm, can_review)

        # Publisher group: can review and publish posts (and change)
        publisher, created = Group.objects.get_or_create(name="publisher")
        publisher.permissions.add(change_perm, can_review, can_publish)

        # Admin-like maintainer group for completeness
        maintainer, created = Group.objects.get_or_create(name="maintainer")
        maintainer.permissions.add(change_perm, delete_perm, can_review, can_publish)

        self.stdout.write(self.style.SUCCESS("Groups created/updated: editor, publisher, maintainer"))
