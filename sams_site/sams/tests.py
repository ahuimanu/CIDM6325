from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Item


User = get_user_model()


class SamsBasicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass')

    def test_item_list_view(self):
        resp = self.client.get(reverse('sams:item_list'))
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        # anonymous should be redirected to login when trying to access create
        resp = self.client.get(reverse('sams:item_create'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp['Location'])

    def test_logged_in_user_can_create_item_and_owner_assigned(self):
        self.client.login(username='alice', password='pass')
        resp = self.client.post(reverse('sams:item_create'), {'title': 'Test', 'description': 'desc'})
        # after create should redirect to detail
        self.assertEqual(resp.status_code, 302)
        item = Item.objects.get(title='Test')
        self.assertEqual(item.owner, self.user)

    def test_register_creates_and_logs_in_user(self):
        resp = self.client.post(reverse('sams:register'), {'username': 'bob', 'password1': 'complexpass1', 'password2': 'complexpass1'})
        # should redirect to index
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='bob').exists())

    def test_search_and_pagination(self):
        # create 15 items to test pagination
        for i in range(15):
            Item.objects.create(title=f'Item {i}', description='desc', owner=self.user)
        resp = self.client.get(reverse('sams:item_list'))
        self.assertEqual(resp.status_code, 200)
        # paginate_by=10 so page 1 should have 10
        self.assertTrue('items' in resp.context)
        self.assertEqual(len(resp.context['items']), 10)
        # search for an item
        resp2 = self.client.get(reverse('sams:item_list') + '?q=Item 14')
        self.assertContains(resp2, 'Item 14')

    def test_edit_delete_permissions(self):
        item = Item.objects.create(title='Owned', description='x', owner=self.user)
        # other user cannot edit/delete
        other = User.objects.create_user(username='other', password='pass')
        self.client.login(username='other', password='pass')
        resp = self.client.get(reverse('sams:item_edit', kwargs={'pk': item.pk}))
        self.assertEqual(resp.status_code, 403)
        resp = self.client.post(reverse('sams:item_delete', kwargs={'pk': item.pk}))
        self.assertEqual(resp.status_code, 403)
        # add other to maintainer group and try again
        from django.contrib.auth.models import Group
        mg, _ = Group.objects.get_or_create(name='maintainer')
        other.groups.add(mg)
        self.client.login(username='other', password='pass')
        resp = self.client.get(reverse('sams:item_edit', kwargs={'pk': item.pk}))
        self.assertEqual(resp.status_code, 200)
        # UI contains Edit/Delete link for maintainer
        resp_detail = self.client.get(reverse('sams:item_detail', kwargs={'pk': item.pk}))
        self.assertContains(resp_detail, 'Edit')
        self.assertContains(resp_detail, 'Delete')
