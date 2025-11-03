from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .auth_forms import CustomUserRegistrationForm, CustomLoginForm


class CustomLoginView(LoginView):
    """
    Custom login view using our styled form
    """
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('blog:index')
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """
    Custom logout view with redirect
    """
    next_page = 'blog:index'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    """
    User registration view using custom form
    """
    form_class = CustomUserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('auth:login')
    
    def form_valid(self, form):
        # Save the user
        response = super().form_valid(form)
        
        # Log the user in automatically after registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        
        if user:
            login(self.request, user)
            messages.success(
                self.request, 
                f'Welcome {username}! Your account has been created successfully.'
            )
            return redirect('blog:index')
        
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


# Function-based views for additional flexibility
@csrf_protect
def custom_login_view(request):
    """
    Function-based login view as an alternative
    """
    if request.user.is_authenticated:
        return redirect('blog:index')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'blog:index')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


@login_required
def custom_logout_view(request):
    """
    Function-based logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('blog:index')


@csrf_protect
def register_view(request):
    """
    Function-based registration view
    """
    if request.user.is_authenticated:
        return redirect('blog:index')
    
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # Automatically log in the user after registration
            login(request, user)
            messages.success(request, f'Welcome {username}! Your account has been created.')
            return redirect('blog:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})