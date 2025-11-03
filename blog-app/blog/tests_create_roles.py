from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Post


class CreateRolesCommandTests(TestCase):
    def test_create_roles_creates_expected_groups_and_permissions(self):
        # Run the management command
        call_command('create_roles')

        # Ensure groups exist
        editor = Group.objects.filter(name='editor').first()
        publisher = Group.objects.filter(name='publisher').first()
        maintainer = Group.objects.filter(name='maintainer').first()
        self.assertIsNotNone(editor, 'editor group should be created')
        self.assertIsNotNone(publisher, 'publisher group should be created')
        self.assertIsNotNone(maintainer, 'maintainer group should be created')

        # Check permissions on Post content type
        ct = ContentType.objects.get_for_model(Post)
        # custom perms declared in Post.Meta
        can_review = Permission.objects.get(content_type=ct, codename='can_review')
        can_publish = Permission.objects.get(content_type=ct, codename='can_publish')
        change_perm = Permission.objects.get(content_type=ct, codename='change_post')
        delete_perm = Permission.objects.get(content_type=ct, codename='delete_post')

        # editor should have change and can_review
        editor_perms = set(p.codename for p in editor.permissions.all())
        self.assertIn('change_post', editor_perms)
        self.assertIn('can_review', editor_perms)

        # publisher should have change, can_review, can_publish
        publisher_perms = set(p.codename for p in publisher.permissions.all())
        self.assertIn('change_post', publisher_perms)
        self.assertIn('can_review', publisher_perms)
        self.assertIn('can_publish', publisher_perms)

        # maintainer should include delete
        maintainer_perms = set(p.codename for p in maintainer.permissions.all())
        self.assertIn('delete_post', maintainer_perms)
        self.assertIn('can_publish', maintainer_perms)
