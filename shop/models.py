from django.db import models
from django.contrib.auth.models import User

User.add_to_class('address', models.CharField(max_length=255, blank=True, null=True))


class Furniture(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shop/images/furniture/')
    dimensions = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    initial_stock = models.PositiveIntegerField(default=0)  # Начальный остаток
    current_stock = models.PositiveIntegerField(default=0)  # Текущий остаток

    def __str__(self):
        return self.name


class Flooring(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shop/images/flooring/')
    dimensions = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    initial_stock = models.PositiveIntegerField(default=0)  # Начальный остаток
    current_stock = models.PositiveIntegerField(default=0)  # Текущий остаток

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shop/images/flooring/')
    dimensions = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"OrderItem #{self.pk}"

