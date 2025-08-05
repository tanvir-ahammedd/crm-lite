from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['user']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
 
class NoHelpTextMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exceptions = getattr(self, 'help_text_exceptions', [])
        for name, field in self.fields.items():
            if name not in exceptions:
                field.help_text = ''
        
class CreateUserForm(NoHelpTextMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
            
        