from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from users.forms import CustomerUserCreationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from users.models_profile import UserProfile
from django.contrib.auth.views import (LoginView, PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView,
                                       PasswordResetConfirmView)

@login_required
def profile_view(request, username):
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        # Обработка случая, если пользователь с указанным именем не найден
        return render(request, 'users/profile_not_found.html')

    # Логика для отображения информации о пользователе
    # Например, если у пользователя есть дополнительные поля профиля:
    profile = user.userprofile  # Предположим, что у пользователя есть связанный профиль
    context = {'user': user, 'profile': profile}

    return render(request, 'users/profile.html', context)



@login_required
def social_login_profile_redirect(request):
    user = request.user
    return redirect(reverse("users:profile", args=[user.username]))

def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "POST":
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # Создаем профиль и сохраняем
            profile = UserProfile.objects.create(user=user, customer_name=form.cleaned_data['customer_name'], address=form.cleaned_data['address'])

            # Отправляем письмо благодарности
            send_thank_you_email(user)

            # Авторизуем пользователя после регистрации
            login(request, user)

            # Перенаправляем на страницу после успешной регистрации
            return redirect(reverse("users:dashboard"))
        else:
            # Форма не валидна, показываем ошибки
            messages.error(request, 'Ошибка при регистрации. Пожалуйста, проверьте введенные данные.')
            return render(request, "users/register.html", {"form": form})
    else:
        # GET запрос - показываем пустую форму
        form = CustomerUserCreationForm()
        return render(request, "users/register.html", {"form": form})


def send_thank_you_email(user, language='uk'):
    subject = "Registration Confirmation"
    if language == 'en':
        message = f"Dear {user.get_full_name()},\n\nThank you for registering on our website."
    else:
        message = f"Dear {user.get_full_name()},\n\nДякуємо за реєстрацію на нашому сайті."

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print("Thank you email sent successfully!")
    except Exception as e:
        print("Failed to send thank you email:", str(e))

# ----------------------------------------


class MyLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_backends = ['social_core.backends.github.GithubOAuth2']  # Указываем бэкенд


class MyPasswordChangeView(PasswordChangeView):
    template_name = "registration/my_password_change_form.html"
    success_url = reverse_lazy("users:password_change_done")


class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "registration/my_password_change_done.html"


class MyPasswordResetView(PasswordResetView):
    template_name = "registration/my_password_reset_form.html"
    success_url = reverse_lazy("users:password_reset_done")
    email_template_name = "registration/my_password_reset_email.html"


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/my_password_reset_done.html"


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("users:my_password_reset_complete")
    template_name = "registration/my_password_reset_confirm.html"


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/my_password_reset_complete.html"