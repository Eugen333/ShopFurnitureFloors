from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from users.forms import CustomerUserCreationForm
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.auth.urls import urlpatterns
from django.contrib.auth.views import (LoginView, PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView,
                                       PasswordResetConfirmView)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def profile_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Обработка случая, если пользователь с указанным именем не найден
        return render(request, 'users/profile_not_found.html')

    # Логика для отображения информации о пользователе
    # Например, если у пользователя есть дополнительные поля профиля:
    profile = user.profile  # Предположим, что у пользователя есть связанный профиль
    context = {'user': user, 'profile': profile}

    return render(request, 'users/profile.html', context)


@login_required
def social_login_profile_redirect(request):
    user = request.user
    return redirect(reverse("users:profile", args=[user.username]))

def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "GET":
        return render(
            request,
            "users/register.html",
            {"form": CustomerUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Указываем бэкенд
            login(request, user)
            send_thank_you_email(user)  # Отправка письма благодарности
            return redirect(reverse("users:dashboard"))


def email_register(request):
    if request.method == "GET":
        return render(
            request,
            "users/register.html",
            {"form": EmailUserCreationForm}
        )
    elif request.method == "POST":
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Указываем бэкенд
            login(request, user)
            send_thank_you_email(user)  # Отправка письма благодарности
            return redirect(reverse("users:dashboard"))



def send_thank_you_email(user):
    subject = "Registration Confirmation"
    message = f"Dear {user.get_full_name()},\n\nДякуємо за реєстрацію на нашому сайті."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    email = EmailMessage(subject, message, from_email, recipient_list)

    try:
        email.send()
        print("Thank you email sent successfully!")
    except Exception as e:
        print("Failed to send thank you email:", str(e))


# def register(request: HttpRequest):
#     if request.method == "GET":
#         return render(
#             request,
#             "users/register.html",
#             {"form": CustomerUserCreationForm}
#         )
#     elif request.method == "POST":
#         form = CustomerUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect(reverse("users:dashboard"))


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


def register(request: HttpRequest):
    if request.method == "POST":
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("users:dashboard"))
    else:
        form = CustomerUserCreationForm()  # Создание пустой формы для GET-запроса

    return render(
        request,
        "users/register.html",
        {"form": form}
    )
