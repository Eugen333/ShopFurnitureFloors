# ShopFurnitureFloors\shop\models.py
from django.db import models
from django.contrib.auth.models import User

User.add_to_class('address', models.CharField(max_length=255, blank=True, null=True))

class ProductManager(models.Manager):
    pass

# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(product_type=self.model.__name__)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shop/images/flooring/')
    dimensions = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0)
    product_type = models.CharField(max_length=20, choices=[('furniture', 'Furniture'), ('flooring', 'Flooring')])

    objects = ProductManager()

    def __str__(self):
        return self.name

class Furniture(Product):
    # id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=100)
    # image = models.ImageField(upload_to='shop/images/furniture/')
    # dimensions = models.CharField(max_length=100)
    # price = models.DecimalField(max_digits=8, decimal_places=2)
    product_ptr = models.OneToOneField(Product, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    initial_stock = models.PositiveIntegerField(default=0)  # Начальный остаток
    current_furniture_stock = models.PositiveIntegerField(default=0)  # Текущий остаток
    # product_type = models.CharField(max_length=20, choices=[('furniture', 'Furniture')])

    # def __str__(self):
    #     return self.name


class Flooring(Product):
    # id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=100)
    # image = models.ImageField(upload_to='shop/images/flooring/')
    # dimensions = models.CharField(max_length=100)
    # price = models.DecimalField(max_digits=8, decimal_places=2)
    product_ptr = models.OneToOneField(Product, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    initial_stock = models.PositiveIntegerField(default=0)  # Начальный остаток
    current_flooring_stock = models.PositiveIntegerField(default=0)  # Текущий остаток
    # product_type = models.CharField(max_length=20, choices=[('flooring', 'Flooring')])

    # def __str__(self):
    #     return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    products = models.ManyToManyField('Product', through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f"Order #{self.pk}"

    def update_stock(self):
        # Метод для уменьшения остатков товаров после создания заказа
        for item in self.orderitem_set.all():
            item.product.current_stock -= item.quantity
            item.product.save()

#  используем промежуточную модель OrderItem для связи многие-ко-многим между Order и Product,
#  чтобы иметь возможность хранить информацию о каждой позиции заказа и ее количестве
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"OrderItem #{self.pk}"

