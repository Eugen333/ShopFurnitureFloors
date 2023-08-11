from django.db import models

class Flooring(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='shop/images/furniture/')
    dimensions = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    initial_stock = models.PositiveIntegerField(default=0)  # Начальный остаток
    current_stock = models.PositiveIntegerField(default=0)  # Текущий остаток

    def __str__(self):
        return self.name
