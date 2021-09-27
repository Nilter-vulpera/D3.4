from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView,DetailView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import Product,Category
from django.views import View
from .filters import ProductFilter, F, C, X
from django.contrib.auth.models import User

class ProductList(ListView):
    model = Product  # указываем модель, объекты которой мы будем выводить
    template_name = 'products.html'  # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'products'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    queryset = Product.objects.order_by("-id")
    ordering = {'-price'}
    context='products'

class ProductDetails(DetailView):
    model = Product
    template_name='products.html'
    context_object_name = 'product'


class Product(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1

    def get_filter(self):
        return ProductFilter(self.request.GET,quryset=super().get_queryset())
    def get_queryset(self):
        return self.get_filter().qs
    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args,**kwargs),
            "filter":self.get_filter(),
        }

    def get(self, request):
            product = Product.objects.order_by('-price')
            p = Paginator(product,1)  # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы

            products = p.get_page(request.GET.get('page', 1))  # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
            # теперь вместо всех объектах в списке товаров хранится только нужная нам страница с товарами

            data = {
                'products': products,
            }
            return render(request, 'templates/flatpages/products.html', data)

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        name = request.POST['name']
        quantity = request.POST['quantity']
        category_id = request.POST['category']
        price = request.POST['price']

        product = Product(name=name, quantity=quantity, category_id=category_id,
                          price=price)  # создаём новый товар и сохраняем
        product.save()
        return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.

def user_list(request):
    f = F(request.GET, queryset=User.objects.all())
    return render(request, 'user_t.html', {'filter': f})


def product_list(request):
    c = C(request.GET, queryset=Product.objects.all())
    return render(request, 'product_t.html', {'filter': c})


def comment_list(request):
    x = X(request.GET, queryset=Comment.objects.all())
    return render(request, 'comment_t.html', {'filter': x})
