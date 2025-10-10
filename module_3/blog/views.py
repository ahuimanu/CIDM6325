from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import HomeDetailsForm
from .models import HomeDetails

def home_details_view(request):
    if request.method == 'POST':
        form = HomeDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Home details submitted successfully!")
            return redirect('/')  # Redirect to the root URL after form submission
    else:
        form = HomeDetailsForm()
    return render(request, 'blog/home_details_form.html', {'form': form})

def home_details_list_view(request):
    entries = HomeDetails.objects.all()
    return render(request, 'blog/home_details_list.html', {'entries': entries})
