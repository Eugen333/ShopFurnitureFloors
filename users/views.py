# ShopFurnitureFloors\users\views.py
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView,
                                       PasswordResetConfirmView)
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import CustomerUserCreationForm
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.core.mail import send_mail
from django.contrib import messages
import social_django.utils
from social_core.exceptions import AuthFailed
from django.http import HttpRequest, HttpResponse
from social_django.utils import load_backend, load_strategy
from django.contrib.auth import get_user_model


def dashboard(request):
    return render(request, "users/dashboard.html")


class MyLoginView(LoginView):
    template_name = "registration/login.html"


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

# ______________________________________________________________________________________________________
# Функция для отправки благодарственного письма после регистрации "почта"
def send_thank_you_email(user):
    sender_email = settings.EMAIL_HOST_USER
    sender_password = settings.EMAIL_HOST_PASSWORD

    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_username = sender_email

    message = MIMEMultipart()
    username = user.username  # Получаем имя пользователя
    message.attach(MIMEText(f"Шановний {username},\n\nдякуємо за реєстрацію на нашому вебсайті. Ми сподіваємося, що вам сподобається ваш досвід!."))

    message["Subject"] = "Ласкаво просимо на наш вебсайт"
    message["From"] = sender_email
    message["To"] = user.email

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, sender_password)
            server.sendmail(sender_email, user.email, message.as_string())
        print("Thank you email sent successfully!")
    except Exception as e:
        print("Failed to send thank you email:", str(e))

# ----------------------------------------
# Регистрация - "почта"
def register(request: HttpRequest):
    if request.method == "POST":
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Отправка благодарственного письма
            send_thank_you_email(user)
            # Явно указываем бэкэнд для аутентификации (используем базовый бэкэнд)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            # Аутентифицируем пользователя
            login(request, user)
            return redirect(reverse("users:dashboard"))
    else:
        form = CustomerUserCreationForm()

    return render(
        request,
        "users/register.html",
        {"form": form}
    )

# Регистрация "Соц"

# ------------------------------------------------------------------------------------------------------------
# только для GitHub
# def social_register(request):
#     if request.method == "POST":
#         strategy = load_strategy(request)
#
#         backend = load_backend(strategy, "github", redirect_uri=None)
#         try:
#             user = backend.auth_complete(request.POST.dict())
#         except AuthFailed as e:
#             # Возникла ошибка аутентификации, обработать ее
#             # Может быть полезно записать эту ошибку для логгирования
#             print("AuthFailed:", str(e))
#             return redirect(reverse("users:login"))  # Перенаправить на страницу логина или другой подходящей странице
#         if user:
#             # Пользователь успешно аутентифицирован через GitHub
#             # Здесь у нас будет объект `user`, представляющий успешно аутентифицированного пользователя
#             # Нужно создать или обновить этого пользователя в базе данных, если это необходимо
#
#             # Пример:
#             User = get_user_model()
#             try:
#                 existing_user = User.objects.get(username=user.username)
#                 # Если пользователь с таким именем уже существует, обновить его данные
#                 existing_user.email = user.email
#                 existing_user.save()
#             except User.DoesNotExist:
#                 # Если пользователя с таким именем нет, создайть нового пользователя
#                 new_user = User(username=user.username, email=user.email)
#                 new_user.save()
#
#             # Вход пользователя (если это необходимо)
#             # Пример:
#             # login(request, new_user)
#
#             # Теперь можно выполнить дополнительные действия, которые нужны после социальной регистрации через GitHub
#             # ...
#
#             # Например, перенаправьте пользователя на домашнюю страницу
#             return redirect(
#                 reverse("users:dashboard"))  # Заменить это на URL-маршрут для домашней страницы пользователя
#
#         # В этом месте можно отобразить форму для социальной регистрации, если это необходимо
#
#     # Возвращает страницу с кнопками для социальной авторизации
#     return render(request, 'users/social_register.html')
# -------------------------------------------------------------------------------------------------------

def social_register(request):
    if request.method == "POST":
        strategy = load_strategy(request)
        # Для GitHub
        github_backend = load_backend(strategy, "github", redirect_uri=None)
        try:
            github_user = github_backend.auth_complete(request.POST.dict())
        except AuthFailed as e:
            print("GitHub AuthFailed:", str(e))
            return redirect(reverse("users:login"))

        # Для Google
        google_backend = load_backend(strategy, "google-oauth2", redirect_uri=None)
        try:
            google_user = google_backend.auth_complete(request.POST.dict())
        except AuthFailed as e:
            print("Google AuthFailed:", str(e))
            return redirect(reverse("users:login"))

        if github_user or google_user:
            User = get_user_model()

            if github_user:
                backend_user = github_user
            else:
                backend_user = google_user

            try:
                existing_user = User.objects.get(username=backend_user.username)
                existing_user.email = backend_user.email
                existing_user.save()
            except User.DoesNotExist:
                new_user = User(username=backend_user.username, email=backend_user.email)
                new_user.save()

            return redirect(reverse("users:dashboard"))

    return render(request, 'users/social_register.html')
# Представление для перенаправления после успешной социальной авторизации
# @login_required
# def social_login_profile_redirect(request):
#     # Проверяем, что пользователь аутентифицирован и пришел с социальной авторизации
#     if request.user.is_authenticated and hasattr(request.user, 'social_auth') and \
#             request.user.social_auth.filter(provider='github').exists():
#         try:
#             # Получение пользователя и email через социальную авторизацию
#             strategy = load_strategy(request)
#             social_user = request.user.social_auth.get(provider='github')
#             github_backend = GithubOAuth2(strategy, social_user)
#             user_info = github_backend.get_user_info()
#             user_email = user_info.get('email')
#         if user_email:
#             # Отправляем приветственное письмо
#             send_welcome_email(user_email)
#     # Перенаправляем пользователя на домашнюю страницу магазина
#     return redirect(reverse("users/social_profile.html"))
# -------------------------------------------------------

# Функция для отправки привітального email
# def send_welcome_email(user_email):
#     # Тема та текст повідомлення
#     subject = "Ласкаво просимо на наш вебсайт"
#     message = "Дякуємо за реєстрацію на нашому вебсайті. Ми сподіваємося, що вам сподобається ваш досвід!"
#
#     # Адреса відправника та отримувача
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user_email]
#
#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         print("Ласкаво просимо email успішно відправлено!")
#     except Exception as e:
#         print("Не вдалося відправити ласкаво просимо email:", str(e))


# Обробка перенаправлення від соціального входу та відправка привітального email
# def social_login_profile_redirect(request):
#     # Обробка перенаправлення від соціального входу та відправка ласкаво просимо email
#     if request.user.is_authenticated:
#         user_email = social_django.utils.user_email(request.user)
#         send_welcome_email(user_email)
#     return redirect(reverse("shop:home"))  # Перенаправлення на домашню сторінку