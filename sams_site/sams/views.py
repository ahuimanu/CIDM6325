from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import calendar
import datetime
import json
from .models import Item, TeamEvent, Student, Attendance
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
    """Admin user registration view.

    Creates an admin user and logs them in, then redirects to the calendar.
    """
    if request.method == 'POST':
        form = SamsUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add user to admin group or mark as staff
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('sams:calendar')
    else:
        form = SamsUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def student_login_view(request):
    """Student login view using Django's authentication."""
    from django.contrib.auth.views import LoginView
    
    class StudentLoginView(LoginView):
        template_name = 'registration/student_login.html'
        
        def get_success_url(self):
            return reverse_lazy('sams:calendar')
    
    return StudentLoginView.as_view()(request)


def student_register(request):
    """Student user registration view.

    Creates a student user and logs them in, then redirects to the calendar.
    """
    if request.method == 'POST':
        form = SamsUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Student users don't get staff privileges
            login(request, user)
            return redirect('sams:calendar')
    else:
        form = SamsUserCreationForm()
    return render(request, 'registration/student_register.html', {'form': form})


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
        
        # Get announcements (latest 5)
        from .models import Announcement
        announcements = Announcement.objects.all().prefetch_related('comments')[:10]
        
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
            'announcements': announcements,
        })
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    """Create a new team event with AJAX support."""
    model = TeamEvent
    fields = ['title', 'description', 'date', 'start_time', 'end_time']
    
    def post(self, request, *args, **kwargs):
        # Check authentication for AJAX requests
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'}, status=401)
        
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                date_str = data.get('date')
                if isinstance(date_str, str):
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                else:
                    date_obj = date_str
                
                # Parse time fields if provided
                start_time = data.get('start_time')
                end_time = data.get('end_time')
                
                # Convert empty strings to None, parse time strings
                if start_time == '' or start_time is None:
                    start_time = None
                elif isinstance(start_time, str):
                    # Parse time string "HH:MM" to time object
                    try:
                        start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
                    except ValueError:
                        start_time = None
                
                if end_time == '' or end_time is None:
                    end_time = None
                elif isinstance(end_time, str):
                    # Parse time string "HH:MM" to time object
                    try:
                        end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
                    except ValueError:
                        end_time = None
                
                event = TeamEvent.objects.create(
                    title=data.get('title', ''),
                    description=data.get('description', ''),
                    date=date_obj,
                    start_time=start_time,
                    end_time=end_time,
                    owner=request.user
                )
                return JsonResponse({
                    'success': True,
                    'event': {
                        'id': event.id,
                        'title': event.title,
                        'description': event.description,
                        'date': event.date.isoformat(),
                        'start_time': event.start_time.strftime('%H:%M') if event.start_time else '',
                        'end_time': event.end_time.strftime('%H:%M') if event.end_time else '',
                        'owner': event.owner.username,
                        'created_at': event.created_at.strftime('%b %d, %Y %I:%M %p'),
                        'has_conflict': event.has_time_conflict()
                    }
                })
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
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
    fields = ['title', 'description', 'date', 'start_time', 'end_time']
    
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
            
            # Update time fields
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            
            # Convert empty strings to None, parse time strings
            if start_time == '' or start_time is None:
                start_time = None
            elif isinstance(start_time, str):
                # Parse time string "HH:MM" to time object
                try:
                    start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
                except ValueError:
                    start_time = None
            
            if end_time == '' or end_time is None:
                end_time = None
            elif isinstance(end_time, str):
                # Parse time string "HH:MM" to time object
                try:
                    end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
                except ValueError:
                    end_time = None
                
            self.object.start_time = start_time
            self.object.end_time = end_time
                
            self.object.save()
            return JsonResponse({
                'success': True,
                'event': {
                    'id': self.object.id,
                    'title': self.object.title,
                    'description': self.object.description,
                    'date': self.object.date.isoformat(),
                    'start_time': self.object.start_time.strftime('%H:%M') if self.object.start_time else '',
                    'end_time': self.object.end_time.strftime('%H:%M') if self.object.end_time else '',
                    'owner': self.object.owner.username,
                    'created_at': self.object.created_at.strftime('%b %d, %Y %I:%M %p'),
                    'has_conflict': self.object.has_time_conflict()
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


# Blog/Announcement Views (Public - no authentication required)
def blog_create(request):
    """Create a new blog post (public)."""
    if request.method == 'POST':
        from .models import Announcement
        Announcement.objects.create(
            title=request.POST.get('title', 'Untitled'),
            content=request.POST.get('content', ''),
            author_name=request.POST.get('author_name', 'Anonymous')
        )
    return redirect('sams:calendar')


def comment_create(request, announcement_id):
    """Add a comment to a blog post (public)."""
    if request.method == 'POST':
        from .models import Announcement, Comment
        try:
            announcement = Announcement.objects.get(id=announcement_id)
            Comment.objects.create(
                announcement=announcement,
                author_name=request.POST.get('author_name', 'Anonymous'),
                content=request.POST.get('content', '')
            )
        except Announcement.DoesNotExist:
            pass
    return redirect('sams:calendar')


def custom_logout(request):
    """Custom logout view that handles both GET and POST requests."""
    logout(request)
    return redirect('login')


def attendance_load(request):
    """Load students and their attendance status for a given date."""
    date_str = request.GET.get('date')
    
    if not date_str:
        return JsonResponse({'error': 'Date parameter required'}, status=400)
    
    try:
        target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    # Get all students
    students = Student.objects.all().order_by('name')
    
    # Get attendance records for this date
    attendance_records = Attendance.objects.filter(date=target_date).select_related('student')
    attendance_map = {record.student_id: record.present for record in attendance_records}
    
    students_data = [
        {
            'id': student.id,
            'name': student.name,
            'student_id': student.student_id or '',
            'present': attendance_map.get(student.id, False)
        }
        for student in students
    ]
    
    return JsonResponse({'students': students_data})


def attendance_save(request):
    """Save attendance records for a given date."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        date_str = data.get('date')
        attendance_list = data.get('attendance', [])
        
        if not date_str:
            return JsonResponse({'error': 'Date required'}, status=400)
        
        target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Save each attendance record
        saved_count = 0
        for item in attendance_list:
            student_id = item.get('student_id')
            present = item.get('present', False)
            
            if not student_id:
                continue
            
            # Update or create attendance record
            Attendance.objects.update_or_create(
                student_id=student_id,
                date=target_date,
                defaults={
                    'present': present,
                    'recorded_by': request.user
                }
            )
            saved_count += 1
        
        return JsonResponse({
            'success': True,
            'saved_count': saved_count,
            'date': date_str
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
