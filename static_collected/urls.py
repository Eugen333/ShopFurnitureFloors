# shop/urls.py

from django.urls import path
from .views import (
    HomeView, FurnitureListView, FlooringListView, FlooringDetailView,
    create_order, order_success, order_view_furniture, order_flooring
)

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('furniture/', FurnitureListView.as_view(), name='furniture'),
    path('flooring/', FlooringListView.as_view(), name='flooring_list'),
    path('flooring/<int:pk>/', FlooringDetailView.as_view(), name='flooring_detail'),
    path('order/<int:pk>/', create_order, name='order'),
    path('order_success/', order_success, name='order_success'),
    path('order/furniture/<int:pk>/', order_view_furniture, name='order_furniture'),
    path('order/flooring/<int:pk>/', order_flooring, name='order_flooring'),
    # path('order/furniture/<int:pk>/', create_order, name='order_furniture'),
]
