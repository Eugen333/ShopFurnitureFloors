# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, FormView
from .models import Furniture, Flooring, Order, OrderItem, Product
from .forms import UserForm, OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import logging

# Оставим описания классов представлений сначала
class HomeView(TemplateView):
    template_name = 'shop/home.html'

class FurnitureListView(ListView):
    model = Furniture
    template_name = 'shop/furniture/furniture.html'
    context_object_name = 'furniture'

# Представление для деталей мебели
class FurnitureDetailView(DetailView):
    model = Furniture
    template_name = 'shop/furniture/furniture_detail.html'
    context_object_name = 'furniture'

# Представление для списка полов
class FlooringListView(ListView):
    model = Flooring
    template_name = 'shop/flooring/flooring_list.html'
    context_object_name = 'floorings'

# Представление для деталей полов
class FlooringDetailView(DetailView):
    model = Flooring
    template_name = 'shop/flooring/flooring_detail.html'
    context_object_name = 'flooring'

# Представление для успешного заказа
class OrderSuccessView(TemplateView):
    template_name = 'shop/order_success.html'
# Общая функция для создания заказа
@login_required(login_url='users:login')
def create_order(request, product, form, product_type):
    if form.is_valid():
        customer_name = form.cleaned_data['customer_name']
        address = form.cleaned_data['address']
        quantity = form.cleaned_data['quantity']
        total_price = product.price * quantity

        if product.current_stock >= quantity:
            # Создаем заказ с указанием текущего пользователя
            order = Order.objects.create(
                user=request.user,
                total_amount=total_price,

            )

            # Создаем OrderItem для этого заказа
            product_instance = Product.objects.get(pk=product.pk)
            OrderItem.objects.create(
                order=order,
                product=product_instance,
                quantity=quantity,
                subtotal=total_price
            )

            # Уменьшаем остатки товаров
            product.current_stock -= quantity
            product.save()

            return render(request, 'shop/order_success.html', {'product_type': product_type})
        else:
            error_message = "На жаль, недостатньо товару на складі."
            return render(request, 'shop/order.html',
                          {'form': form, 'product': product, 'product_type': product_type, 'error_message': error_message})
    else:
        messages.error(request, "Invalid form data")
        return render(request, 'shop/order.html', {'form': form, 'product': product, 'product_type': product_type})

# Представление для оформления заказа
@login_required(login_url='users:register')
def order_view(request, pk, product_type):
    # Выводим значение pk в консоль для отладки
    logger = logging.getLogger(__name__)
    logger.debug("Received pk value: %s", pk)
    if product_type == 'furniture':
        product_model = Furniture
    elif product_type == 'flooring':
        product_model = Flooring
    else:
        return redirect('shop:home')

    product = get_object_or_404(product_model, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            return create_order(request, product, form, product_type=product_type)
    else:
        form = OrderForm()

    return render(request, 'shop/order.html', {'form': form, 'product': product, 'product_type': product_type})


# Классы FormView для оформления заказа мебели
class FurnitureOrderFormView(FormView):
    form_class = OrderForm
    template_name = 'shop/order.html'

    def form_valid(self, form):
        furniture = get_object_or_404(Furniture, pk=self.kwargs['pk'])
        return create_order(self.request, furniture, form, product_type='furniture')

# Классы FormView для оформления заказа полов
class FlooringOrderFormView(FormView):
    form_class = OrderForm
    template_name = 'shop/order.html'

    def form_valid(self, form):
        try:
            flooring = Flooring.objects.get(pk=self.kwargs['pk'])
            return create_order(self.request, flooring, form, product_type='flooring')
        except Flooring.DoesNotExist:
            return redirect('shop:flooring_list')

