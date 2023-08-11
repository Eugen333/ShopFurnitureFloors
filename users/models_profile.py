from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    # Один к одному с кастомной моделью пользователя (CustomUser)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)