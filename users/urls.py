from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),  # URL для страницы входа
    path('dashboard/', views.dashboard, name='dashboard'),  # URL для страницы "dashboard"
    path('register/', views.register, name='register'),  # URL для страницы регистрации
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('social-login-profile-redirect/', views.social_login_profile_redirect, name='social_login_profile_redirect'),
]