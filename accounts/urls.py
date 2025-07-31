from django.urls import path

from .views import home, customer, products, createOrder, updateOrder, deleteOrder

urlpatterns = [
    path('', home, name='home'),
    path('customer/<int:pk>', customer, name="customer"),
    path('products/', products, name="products"),
    
    path('create-order/<int:pk>', createOrder, name="create-order"),
    path('update-order/<int:pk>', updateOrder, name='update-order'),
    path('delete-order/<int:pk>', deleteOrder, name='delete-order'),
]
