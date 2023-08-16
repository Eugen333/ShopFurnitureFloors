
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Furniture, Order, OrderItem
from .forms import UserForm, OrderForm
from .models import Flooring
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

class HomeView(TemplateView):
    template_name = 'shop/home.html'


class FurnitureListView(ListView):
    model = Furniture
    template_name = 'shop/furniture/furniture.html'
    context_object_name = 'furniture'

    def post(self, request, *args, **kwargs):
        # Отримати дані з POST-запиту
        form = UserForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()

            # Отримати дані з форми
            customer_name = user_form.first_name
            email = user_form.email
            address = user_form.address
            quantity = form.cleaned_data['quantity']

            # Отримати об'єкт меблів з контексту ListView (self.object_list)
            furniture = self.object_list.get(pk=self.kwargs['pk'])

            total_price = furniture.price * quantity

            # Перевіряємо, чи достатньо товару на складі
            if furniture.current_stock >= quantity:
                order = Order.objects.create(
                    customer_name=customer_name,
                    email=email,
                    address=address,
                    total_price=total_price
                )
                OrderItem.objects.create(
                    order=order,
                    product=furniture,
                    quantity=quantity
                )

                # Зменшуємо кількість товару на складі відповідно до кількості замовленого
                furniture.current_stock -= quantity
                furniture.save()

                # Перенаправляємо користувача на сторінку успішного замовлення
                return render(request, 'shop/order_success.html')
            else:
                # Якщо товару не вистачає на складі, показуємо повідомлення про помилку
                error_message = "На жаль, недостатньо товару на складі."
                return render(request, 'shop/order.html',
                              {'form': form, 'product': furniture, 'error_message': error_message})
        else:
            # Якщо дані форми недійсні, відображаємо помилку
            messages.error(request, "Invalid form data")
            return self.get(request, *args, **kwargs)

class FurnitureDetailView(DetailView):
    model = Furniture
    template_name = 'shop/furniture/furniture_detail.html'
    context_object_name = 'furniture'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm()  # Використовуємо OrderForm для замовлення
        return context


class FlooringListView(ListView):
    model = Flooring
    template_name = 'shop/flooring/flooring_list.html'
    context_object_name = 'floorings' # Змінна 'floorings' передається у шаблон


class FlooringDetailView(DetailView):
    model = Flooring
    template_name = 'shop/flooring/flooring_detail.html'
    context_object_name = 'flooring'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm()  # Використовуємо OrderForm для замовлення
        return context


def home_view(request):
    user_form = UserForm()
    context = {
        'user_form': user_form,
    }
    return render(request, 'shop/home.html')


# -----------------------------------------------------------------------------------------------
# Використовуємо декоратор для забезпечення доступу лише зареєстрованим користувачам

def create_order(request, pk):
    # Отримати об'єкт меблів за переданим pk або показати 404 сторінку, якщо меблі не знайдені
    furniture = get_object_or_404(Furniture, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()

            customer_name = user_form.first_name
            email = user_form.email
            address = user_form.address
            quantity = form.cleaned_data['quantity']
            total_price = furniture.price * quantity

            # Перевіряємо, чи достатньо товару на складі
            if furniture.current_stock >= quantity:
                order = Order.objects.create(
                    customer_name=customer_name,
                    email=email,
                    address=address,
                    total_price=total_price
                )
                OrderItem.objects.create(
                    order=order,
                    product=furniture,
                    quantity=quantity
                )

                # Зменшуємо кількість товару на складі відповідно до кількості замовленого
                furniture.current_stock -= quantity
                furniture.save()

                # Перенаправляємо користувача на сторінку успішного замовлення
                return render(request, 'shop/order_success.html')
            else:
                # Якщо товару не вистачає на складі, показуємо повідомлення про помилку
                error_message = "На жаль, недостатньо товару на складі."
                return render(request, 'shop/order.html',
                              {'form': form, 'product': furniture, 'error_message': error_message})
    else:
        form = UserForm()

    # Перенаправляємо неаутентифікованих користувачів на сторінку реєстрації
    if not request.user.is_authenticated:
        return redirect('users:register')

    return render(request, 'shop/order.html', {'form': form, 'product': furniture})


def order_view_furniture(request, pk):
    furniture = get_object_or_404(Furniture, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            customer_name = form.cleaned_data['customer_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            quantity = form.cleaned_data['quantity']
            total_price = furniture.price * quantity

            # Проверяем, достаточно ли товара на складе
            if furniture.current_stock >= quantity:
                order = Order.objects.create(
                    customer_name=customer_name,
                    email=email,
                    address=address,
                    total_price=total_price
                )
                OrderItem.objects.create(
                    order=order,
                    product=furniture,
                    quantity=quantity
                )
                # Уменьшаем количество товара на складе в соответствии с заказом
                furniture.current_stock -= quantity
                furniture.save()
                # Перенаправляем пользователя на страницу успешного заказа
                return render(request, 'shop/order_success.html')
            else:
                # Если товара не хватает на складе, показываем сообщение об ошибке
                error_message = "На жаль, недостатньо товару на складі."
                return render(request, 'shop/order.html',
                              {'form': form, 'product': furniture, 'error_message': error_message})
    else:
        form = OrderForm()

    # Перенаправляем неаутентифицированных пользователей на страницу регистрации
    if not request.user.is_authenticated:
        return redirect('users:register')

    return render(request, 'shop/order.html', {'form': form, 'product': furniture})

# ----------------------------------------------------------------------------------------------

@login_required(login_url='users:register')  # Если пользователь не аутентифицирован, перенаправлять на страницу регистрации
def order_flooring(request, pk):
    try:
        flooring = Flooring.objects.get(pk=pk)
        # Здесь можно добавить логику оформления заказа, например, сохранение заказа в базе данных и т.п.
        context = {'flooring': flooring}
        return render(request, 'shop/order.html', context)
    except Flooring.DoesNotExist:
        # Обработка случая, если товар не найден
        return redirect('shop:flooring_list')


# Подтверждение успешного заказа
def order_success(request):
    return render(request, 'shop/order_success.html')
