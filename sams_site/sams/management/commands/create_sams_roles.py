from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from sams.models import Item


class Command(BaseCommand):
    help = 'Create SAMS roles and assign basic model permissions'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Item)
        perms = Permission.objects.filter(content_type=content_type)
        # Create groups
        editor, _ = Group.objects.get_or_create(name='editor')
        maintainer, _ = Group.objects.get_or_create(name='maintainer')
        # Assign permissions: editors can add/change, maintainers can delete/change
        add_perm = perms.get(codename='add_item')
        change_perm = perms.get(codename='change_item')
        delete_perm = perms.get(codename='delete_item')
        editor.permissions.add(add_perm, change_perm)
        maintainer.permissions.add(change_perm, delete_perm)
        self.stdout.write(self.style.SUCCESS('Created groups and assigned permissions'))
