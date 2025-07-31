from django.urls import path

from .views import home, customer, products

urlpatterns = [
    path('', home, name='home'),
    path('customer/<int:pk>', customer, name="customer"),
    path('products/', products, name="products"),
]
