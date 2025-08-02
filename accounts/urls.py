from django.urls import path

from .views import *

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    
    path('', home, name='home'),
    path('customer/<int:pk>', customer, name="customer"),
    path('products/', products, name="products"),
    
    path('create-order/<int:pk>', createOrder, name="create-order"),
    path('update-order/<int:pk>', updateOrder, name='update-order'),
    path('delete-order/<int:pk>', deleteOrder, name='delete-order'),
    
]
