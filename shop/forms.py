# ShopFurnitureFloors\shop\forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Order, Product, Flooring, Furniture

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'address', 'quantity']

    customer_name = forms.CharField(label='Имя', max_length=100)
    address = forms.CharField(label='Адрес', max_length=200)
    quantity = forms.IntegerField(label='Количество', min_value=1)

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

class ProductOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # Здесь пустой список, так как некоторые поля будут добавлены вручную

    customer_name = forms.CharField(label='Ім\'я', max_length=100)
    address = forms.CharField(label='Адреса', max_length=200)
    email = forms.EmailField(label='Email')
    flooring_product = forms.ModelChoiceField(queryset=Flooring.objects.all(), label='Пол', required=False)
    furniture_product = forms.ModelChoiceField(queryset=Furniture.objects.all(), label='Мебель', required=False)
    quantity = forms.IntegerField(label='Кількість', min_value=1)
