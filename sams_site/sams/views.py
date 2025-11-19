from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import calendar
import datetime
import json
from .models import Item, TeamEvent
from .forms import SamsUserCreationForm


class ItemListView(ListView):
    model = Item
    template_name = 'sams/item_list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)
        return qs

class ItemDetailView(DetailView):
    model = Item
    template_name = 'sams/item_detail.html'
    context_object_name = 'item'


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'description']
    template_name = 'sams/item_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('sams:item_detail', kwargs={'pk': self.object.pk})


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['title', 'description']
    template_name = 'sams/item_form.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        # owner can edit or users in 'maintainer' group
        return obj.owner == user or user.groups.filter(name='maintainer').exists()

    def get_success_url(self):
        return reverse_lazy('sams:item_detail', kwargs={'pk': self.object.pk})


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'sams/item_confirm_delete.html'
    success_url = reverse_lazy('sams:item_list')

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.owner == user or user.groups.filter(name='maintainer').exists()


def register(request):
    """Simple user registration view using Django's UserCreationForm.

    Creates a user and logs them in, then redirects to the SAMS index.
    """
    if request.method == 'POST':
        form = SamsUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sams:calendar')
    else:
        form = SamsUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class CalendarView(TemplateView):
    """Dynamic team calendar view with month/year navigation and interactive date cells."""
    template_name = 'sams/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current month/year or from query params
        today = timezone.localdate()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        
        # Create calendar data
        cal = calendar.Calendar(firstweekday=6)  # Start with Sunday
        month_days = list(cal.monthdayscalendar(year, month))
        
        # Get events for this month
        start_date = datetime.date(year, month, 1)
        if month == 12:
            end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
            
        events = TeamEvent.objects.filter(date__range=(start_date, end_date))
        events_by_date = {}
        for event in events:
            if event.date not in events_by_date:
                events_by_date[event.date] = []
            events_by_date[event.date].append(event)
        
        # Navigation dates
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        
        context.update({
            'year': year,
            'month': month,
            'month_name': calendar.month_name[month],
            'month_days': month_days,
            'events_by_date': events_by_date,
            'today': today,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
        })
        return context


@method_decorator(csrf_exempt, name='dispatch')
class EventCreateView(LoginRequiredMixin, CreateView):
    """Create a new team event with AJAX support."""
    model = TeamEvent
    fields = ['title', 'description', 'date']
    
    def post(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            date_str = data.get('date')
            if isinstance(date_str, str):
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                date_obj = date_str
            
            event = TeamEvent.objects.create(
                title=data.get('title', ''),
                description=data.get('description', ''),
                date=date_obj,
                owner=request.user
            )
            return JsonResponse({
                'success': True,
                'event': {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'date': event.date.isoformat(),
                    'owner': event.owner.username
                }
            })
        else:
            # Regular form submission
            form = self.get_form()
            if form.is_valid():
                form.instance.owner = request.user
                return self.form_valid(form)
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('sams:calendar')


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing team event with AJAX support."""
    model = TeamEvent
    fields = ['title', 'description', 'date']
    
    def test_func(self):
        # Allow all authenticated users to edit any event per requirement
        return True
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            self.object.title = data.get('title', self.object.title)
            self.object.description = data.get('description', self.object.description)
            
            date_str = data.get('date', self.object.date)
            if isinstance(date_str, str):
                self.object.date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                self.object.date = date_str
                
            self.object.save()
            return JsonResponse({
                'success': True,
                'event': {
                    'id': self.object.id,
                    'title': self.object.title,
                    'description': self.object.description,
                    'date': self.object.date.isoformat(),
                    'owner': self.object.owner.username
                }
            })
        else:
            return super().post(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('sams:calendar')


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a team event with AJAX support."""
    model = TeamEvent
    template_name = 'sams/teamevent_confirm_delete.html'
    
    def test_func(self):
        # Allow all authenticated users to delete any event per requirement
        return True
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.content_type == 'application/json' or request.method == 'DELETE':
            self.object.delete()
            return JsonResponse({'success': True})
        else:
            return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('sams:calendar')
