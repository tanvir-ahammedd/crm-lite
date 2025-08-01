from django.shortcuts import render
from django.shortcuts import redirect
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm
from .filters import OrderFilter

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count
    
    context = {'orders': orders, 'customers': customers, 'delivered': delivered,
               'pending': pending, 'total_orders': total_orders}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    
    context = {'customer': customer, 'orders': orders,
                'total_orders': total_orders, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
    parent_model=Customer,     # Parent
    model=Order,               # Child
    fields=('product', 'status'),  # Fields to edit
    extra=5                    # Number of blank forms to show
    )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer': customer}) # pre-fill the customer field
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'accounts/order_form.html', {'form': form})

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    return render(request, 'accounts/delete.html', {'order': order})