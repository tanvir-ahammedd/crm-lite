from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    
    path('user/', userPage, name='user-page'),
    path('account/', accountSettings, name="account"),
    
    path('', home, name='home'),
    path('customer/<int:pk>', customer, name="customer"),
    path('products/', products, name="products"),
    
    path('create-order/<int:pk>', createOrder, name="create-order"),
    path('update-order/<int:pk>', updateOrder, name='update-order'),
    path('delete-order/<int:pk>', deleteOrder, name='delete-order'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"), name="reset_password"),
    path('reset_password_set/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
    
]

'''
1 - Submit email form                    // PasswordResetView.as_view()
2 - Email sent success message          // PasswordResetDoneView.as_view()
3 - Link to password reset form in email // PasswordResetConfirmView.as_view()
4 - Password successfully changed message // PasswordResetCompleteView.as_view()

'''
