from django import forms
from .models import Flooring
from .models import Furniture
from django.contrib.auth.models import User

class FlooringForm(forms.ModelForm):
    class Meta:
        model = Flooring
        fields = ['name', 'image', 'dimensions', 'price']

class FurnitureForm(forms.ModelForm):
    class Meta:
        model = Furniture
        fields = ['name', 'image', 'dimensions', 'price']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address']

class OrderForm(forms.Form):
    customer_name = forms.CharField(label='Ім\'я', max_length=100)
    address = forms.CharField(label='Адреса', max_length=200)
    email = forms.EmailField(label='Email')
    quantity = forms.IntegerField(label='Кількість', min_value=1)
