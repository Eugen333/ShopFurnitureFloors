# shop/urls.py

from django.urls import path
from .views import (
    HomeView, FurnitureListView, FlooringListView,
    create_order, order_success, order_view_furniture
)

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('furniture/', FurnitureListView.as_view(), name='furniture'),
    path('flooring/', FlooringListView.as_view(), name='flooring_list'),
    path('order/<int:pk>/', create_order, name='order_product'),
    path('order_success/', order_success, name='order_success'),
    path('order/furniture/<int:pk>/', order_view_furniture, name='order_furniture'),
    # path('order/furniture/<int:pk>/', create_order, name='order_furniture'),
]
