from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from .models import Item
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
            return redirect('sams:item_list')
    else:
        form = SamsUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
