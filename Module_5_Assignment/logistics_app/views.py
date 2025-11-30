# logistics_app/views.py


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Order, Customer
from .forms import OrderForm, CustomerForm
from .ai_engine import calculate_eta_mock
from django.shortcuts import render
from django.http import HttpResponse
# Home/index view
def index(request):
    form = OrderForm()
    return render(request, 'index.html', {'form': form})

# Optional endpoint for testing ETA
def predict_eta(request):
    eta = calculate_eta_mock(None)
    return HttpResponse(eta)

class CustomerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "logistics_app/customer_form.html"
    success_url = reverse_lazy("order_create")  # or wherever you want to redirect
    success_message = "✅ Customer created successfully!"
    
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "logistics_app/order_list.html"
    context_object_name = "orders"
    ordering = ["-order_date"]


class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Allows authenticated users to create a new order."""
    model = Order
    form_class = OrderForm
    template_name = "logistics_app/order_form.html"
    success_url = reverse_lazy("order_list")
    success_message = "✅ Order created successfully!"

    def form_valid(self, form):
        order = form.save(commit=False)
        order.eta = calculate_eta_mock(order)
        order.created_by = self.request.user
        order.save()
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Allows editing an existing order."""
    model = Order
    form_class = OrderForm
    template_name = "logistics_app/order_form.html"
    success_url = reverse_lazy("order_list")
    success_message = "✅ Order updated successfully!"

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """Handles deletion of an order."""
    model = Order
    template_name = "logistics_app/order_confirm_delete.html"
    success_url = reverse_lazy("order_list")
    success_message = "✅ Order deleted successfully!" 
   
