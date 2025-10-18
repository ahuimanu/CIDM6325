# logistics_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import OrderForm
from .models import Order
from .ai_engine import calculate_eta_mock

# Home/index view
def index(request):
    form = OrderForm()
    return render(request, 'index.html', {'form': form})

# Optional endpoint for testing ETA
def predict_eta(request):
    eta = calculate_eta_mock(None)
    return HttpResponse(eta)

# Create new order
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.eta = calculate_eta_mock(order)
            order.save()

            if request.htmx:
                return HttpResponse(
                    f'<div class="alert alert-success">✅ Order <strong>{order.order_id}</strong> created successfully with ETA: <strong>{order.eta}</strong>.</div>'
                )
            return redirect('/orders/')
    else:
        form = OrderForm()

    return render(request, 'logistics_app/order_form.html', {
        'form': form,
        'is_update': False,
    })

# List all orders
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'logistics_app/order_list.html', {'orders': orders})

# Update an existing order
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order, read_only=True)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order, read_only=True)

    return render(request, 'logistics_app/order_form.html', {
        'form': form,
        'is_update': True,
    })

# Delete an order
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/orders/')
    return render(request, 'logistics_app/order_confirm_delete.html', {'order': order})
