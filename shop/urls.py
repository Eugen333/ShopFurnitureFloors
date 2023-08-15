# shop/urls.py

from django.contrib import admin
from django.urls import path
from . import views
from .views import (
    HomeView, FlooringListView, FlooringDetailView, FurnitureListView, FurnitureDetailView,
    FurnitureOrderFormView, FlooringOrderFormView, OrderSuccessView,
)

app_name = 'shop'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('furniture/', FurnitureListView.as_view(), name='furniture'),
    # path('order/furniture/<int:pk>/', FurnitureOrderFormView.as_view(), name='order_furniture_form'),
    path('furniture/<int:pk>/', FurnitureDetailView.as_view(), name='furniture_detail'),
    path('flooring/', FlooringListView.as_view(), name='flooring_list'),
    path('flooring/<int:pk>/', FlooringDetailView.as_view(), name='flooring_detail'),
    # Оформление заказов
    path('order/<str:product_type>/<int:pk>/', views.order_view, name='order'),
    # Страница успешного заказа
    path('order/success/', OrderSuccessView.as_view(), name='order_success'),
]
