from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager




# Кастомный менеджер для кастомной модели пользователя
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Проверка наличия прав is_staff и is_superuser
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Создание суперпользователя
        return self.create_user(username, email, password, **extra_fields)

# Создаем кастомную модель пользователя (CustomUser)
class CustomUser(AbstractUser):
    # Дополнительные поля для кастомной модели пользователя
    customer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    # Подключаем кастомный менеджер
    objects = CustomUserManager()

    # Обязательные поля для входа и аутентификации
    REQUIRED_FIELDS = ['email', 'customer_name', 'address']