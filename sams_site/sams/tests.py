import json
import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Item, TeamEvent


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
        # should redirect to calendar (main page)
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


class CalendarTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.today = timezone.localdate()

    def test_calendar_view_loads(self):
        """Test that the calendar view loads successfully."""
        resp = self.client.get(reverse('sams:calendar'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Team Calendar')

    def test_calendar_navigation(self):
        """Test month/year navigation in calendar."""
        # Test current month
        resp = self.client.get(reverse('sams:calendar'))
        self.assertContains(resp, self.today.strftime('%B'))
        
        # Test previous month navigation
        prev_month = self.today.month - 1 if self.today.month > 1 else 12
        prev_year = self.today.year if self.today.month > 1 else self.today.year - 1
        resp = self.client.get(reverse('sams:calendar') + f'?year={prev_year}&month={prev_month}')
        self.assertEqual(resp.status_code, 200)

    def test_event_creation_ajax(self):
        """Test creating events via AJAX."""
        self.client.login(username='testuser', password='testpass')
        
        event_data = {
            'title': 'Test Event',
            'description': 'Test Description',
            'date': self.today.isoformat()
        }
        
        resp = self.client.post(
            reverse('sams:event_create'),
            data=json.dumps(event_data),
            content_type='application/json'
        )
        
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['event']['title'], 'Test Event')
        
        # Verify event was created in database
        event = TeamEvent.objects.get(title='Test Event')
        self.assertEqual(event.owner, self.user)
        self.assertEqual(event.date, self.today)

    def test_event_creation_form(self):
        """Test creating events via form submission."""
        self.client.login(username='testuser', password='testpass')
        
        resp = self.client.post(reverse('sams:event_create'), {
            'title': 'Form Event',
            'description': 'Form Description',
            'date': self.today.isoformat()
        })
        
        self.assertEqual(resp.status_code, 302)  # Redirect after creation
        self.assertTrue(TeamEvent.objects.filter(title='Form Event').exists())

    def test_event_update_ajax(self):
        """Test updating events via AJAX."""
        self.client.login(username='testuser', password='testpass')
        
        # Create an event first
        event = TeamEvent.objects.create(
            title='Original Title',
            description='Original Description',
            date=self.today,
            owner=self.user
        )
        
        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'date': self.today.isoformat()
        }
        
        resp = self.client.post(
            reverse('sams:event_edit', kwargs={'pk': event.pk}),
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['event']['title'], 'Updated Title')
        
        # Verify event was updated in database
        event.refresh_from_db()
        self.assertEqual(event.title, 'Updated Title')

    def test_event_delete_ajax(self):
        """Test deleting events via AJAX."""
        self.client.login(username='testuser', password='testpass')
        
        # Create an event first
        event = TeamEvent.objects.create(
            title='To Delete',
            description='Will be deleted',
            date=self.today,
            owner=self.user
        )
        
        resp = self.client.delete(
            reverse('sams:event_delete', kwargs={'pk': event.pk}),
            content_type='application/json'
        )
        
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        
        # Verify event was deleted from database
        self.assertFalse(TeamEvent.objects.filter(pk=event.pk).exists())

    def test_event_permissions(self):
        """Test that all authenticated users can edit/delete events per requirement."""
        # Create event with first user
        self.client.login(username='testuser', password='testpass')
        event = TeamEvent.objects.create(
            title='Shared Event',
            date=self.today,
            owner=self.user
        )
        
        # Create second user and login
        other_user = User.objects.create_user(username='other', password='testpass')
        self.client.login(username='other', password='testpass')
        
        # Other user should be able to edit
        resp = self.client.get(reverse('sams:event_edit', kwargs={'pk': event.pk}))
        self.assertEqual(resp.status_code, 200)
        
        # Other user should be able to delete
        resp = self.client.delete(
            reverse('sams:event_delete', kwargs={'pk': event.pk}),
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)

    def test_calendar_displays_events(self):
        """Test that events appear on the calendar."""
        self.client.login(username='testuser', password='testpass')
        
        # Create an event for today
        event = TeamEvent.objects.create(
            title='Display Test',
            description='Should appear on calendar',
            date=self.today,
            owner=self.user
        )
        
        resp = self.client.get(reverse('sams:calendar'))
        self.assertContains(resp, 'Display Test')

    def test_events_require_authentication(self):
        """Test that anonymous users cannot create/edit/delete events."""
        # Try to create event without login
        resp = self.client.post(reverse('sams:event_create'), {
            'title': 'Anonymous Event',
            'date': self.today.isoformat()
        })
        self.assertEqual(resp.status_code, 302)  # Redirect to login
        
        # Create event for edit/delete tests
        event = TeamEvent.objects.create(
            title='Test Event',
            date=self.today,
            owner=self.user
        )
        
        # Try to edit without login
        resp = self.client.get(reverse('sams:event_edit', kwargs={'pk': event.pk}))
        self.assertEqual(resp.status_code, 302)  # Redirect to login
        
        # Try to delete without login
        resp = self.client.delete(reverse('sams:event_delete', kwargs={'pk': event.pk}))
        self.assertEqual(resp.status_code, 302)  # Redirect to login
