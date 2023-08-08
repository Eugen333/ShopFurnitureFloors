# shop/urls.py

from django.urls import path, include
from .views import (
    HomeView, FlooringListView, FurnitureListView,
    FlooringDetailView, order_view, order_view_flooring,
    order_success, furniture_view,
    # dashboard_view,

)

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # URL для домашньої сторінки
    # path('dashboard/', dashboard_view, name='dashboard'),
    path('furniture/', FurnitureListView.as_view(), name='furniture'),
    path('flooring/', FlooringListView.as_view(), name='flooring_list'),
    path('flooring/<int:pk>/', FlooringDetailView.as_view(), name='flooring_detail'),
    path('order/<int:pk>/', order_view, name='order'),
    path('flooring/order/<int:pk>/', order_view_flooring, name='flooring_order'),
    path('order_success/', order_success, name='order_success'),
    path('furniture/<int:pk>/', furniture_view, name='furniture_detail'),
    # path('login/', UserLoginView.as_view(), name='login'),  # URL для сторінки входу
    # path('register/', UserRegisterView.as_view(), name='register'),  # URL для сторінки реєстрації
    # path('accounts/', include('allauth.urls')),  # шлях для включення усіх шляхів allauth
]
