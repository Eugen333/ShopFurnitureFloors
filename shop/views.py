from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Furniture, Flooring, Order, OrderItem, Product
from .forms import UserForm, OrderForm


class FlooringListView(ListView):
    model = Flooring
    template_name = 'shop/flooring/flooring_list.html'
    context_object_name = 'floorings' # Змінна 'furniture' передається у шаблон

class HomeView(TemplateView):
    template_name = 'shop/home.html'

class FurnitureListView(ListView):
    model = Furniture
    template_name = 'shop/furniture/furniture.html'
    context_object_name = 'furniture'

class FlooringDetailView(DetailView):
    model = Flooring
    template_name = 'shop/flooring/flooring_detail.html'
    context_object_name = 'flooring'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm()  # Використовуємо OrderForm для замовлення
        return context

# class UserLoginView(LoginView):
#     template_name = 'shop/registration/login.html'  # Шаблон для сторінки входу
#     success_url = reverse_lazy('shop:home')  # URL, куди перенаправити користувача після успішного входу
#
# class UserRegisterView(CreateView):
#     template_name = 'shop/registration/register.html'  # Шаблон для сторінки реєстрації
#     form_class = UserCreationForm  # Використовуємо стандартну форму для реєстрації користувача
#     success_url = reverse_lazy('shop:home')  # URL, куди перенаправити користувача після успішної реєстрації

# Використовуємо декоратор для забезпечення доступу лише зареєстрованим користувачам
@login_required
def order_view_flooring(request, pk):
    # Отримати об'єкт підлоги за допомогою його ідентифікатора
    flooring = Flooring.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            # Отримати дані з форми
            customer_name = user_form.first_name
            email = user_form.email
            address = user_form.address
            quantity = form.cleaned_data['quantity']
            total_price = flooring.price * quantity
            # Зберегти дані замовлення у базі даних
            order = Order.objects.create(
                customer_name=customer_name,
                email=email,
                address=address,
                total_price=total_price
            )
            # Створити елемент замовлення для зв'язку підлоги і замовлення
            order_item = OrderItem.objects.create(
                order=order,
                product=flooring,
                quantity=quantity
            )
            # Зменшити кількість на складі відповідно до кількості замовленого товару
            flooring.stock -= quantity
            flooring.save()
            return render(request, 'shop/order_success.html')
    else:
        form = UserForm()
    return render(request, 'shop/order.html', {'form': form, 'product': flooring})


@login_required
def order_view_furniture(request, pk):
    furniture = Furniture.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            # Отримати дані з форми
            customer_name = user_form.first_name
            email = user_form.email
            address = user_form.address
            quantity = form.cleaned_data['quantity']
            total_price = furniture.price * quantity
            # Зберегти дані замовлення у базі даних
            order = Order.objects.create(
                customer_name=customer_name,
                email=email,
                address=address,
                total_price=total_price
            )
            # Створити елемент замовлення для зв'язку продукту і замовлення
            order_item = OrderItem.objects.create(
                order=order,
                product=furniture,
                quantity=quantity
            )
            # Зменшити кількість на складі відповідно до кількості замовленого товару
            furniture.stock -= quantity
            furniture.save()
            return render(request, 'shop/order_success.html')
    else:
        form = UserForm()
    return render(request, 'shop/order.html', {'form': form, 'product': furniture})


def order_success(request):
    return render(request, 'shop/order_success.html')


def furniture_view(request):
    furniture = Furniture.objects.all()  # Отримуємо всі об'єкти моделі Furniture
    return render(request, 'shop/furniture/furniture.html', {'furniture': furniture})


def home_view(request):
    user_form = UserForm()
    context = {
        'user_form': user_form,
    }
    return render(request, 'shop/home.html')


def order_view(request, pk):
    # Отримати продукт за допомогою pk або відобразити 404 сторінку, якщо продукт не знайдено
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # Отримати дані з форми оформлення замовлення
        form = OrderForm(request.POST)
        if form.is_valid():
            # Зберегти замовлення
            customer_name = form.cleaned_data['customer_name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']  # Отримуємо email з форми
            quantity = form.cleaned_data['quantity']
            total_price = product.price * quantity

            order = Order.objects.create(
                customer_name=customer_name,
                address=address,
                email=email,  # Зберігаємо email в замовленні
                total_price=total_price,
            )

            # Зберегти деталі замовлення
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )

            return redirect('shop:order_success')  # Перенаправлення на сторінку успішного замовлення

    else:
        # Якщо метод GET, відобразити сторінку з формою
        form = OrderForm()
        return render(request, 'shop/order.html', {'form': form, 'product': product})


# @login_required
# def dashboard_view(request):
#     return render(request, 'shop/dashboard.html')
