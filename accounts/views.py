from django.shortcuts import render
from django.shortcuts import redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

# Create your views here.
def loginPage(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data = request.POST)
            if form.is_valid():
                # name = form.cleaned_data['username']
                name = request.POST.get('username')
                # userpass = form.cleaned_data['password']
                userpass = request.POST.get('password')
                user = authenticate(username = name, password = userpass)
                
                if user is not None:
                    login(request, user) 
                    return redirect('home')
                else:
                    messages.info(request, "Username or Password is Incorrect.") #isn't working this     
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect('home')

def registerPage(request):
    if not request.user.is_authenticated:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                
                if user is not None:
                    login(request, user)
                    name = request.POST.get('username')
                    messages.success(request, "Account is created succesfully for " + name)
                    return redirect(home)
                
        
        context = {'form': form}
        return render(request, 'accounts/register.html', context)
    else:
        return redirect('home')
  
def logoutPage(request):
    logout(request)
    return redirect('login')          

@login_required(login_url='login')
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

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()
    
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    
    context = {'customer': customer, 'orders': orders,
                'total_orders': total_orders, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'accounts/order_form.html', {'form': form})

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('home')
    return render(request, 'accounts/delete.html', {'order': order})