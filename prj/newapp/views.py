from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Product, Comment
from django.core.paginator import Paginator
from .filters import ProductFilter, F, C, X
from django.contrib.auth.models import User
from .forms import ProductForm


# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1

    def get_filter(self):
        return ProductFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

class Default(ListView):
    model = Product
    template_name = 'default.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1

    def get_filter(self):
        return ProductFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }




def Default(request):
    c = C(request.GET, queryset=Product.objects.all())
    return render(request, 'flatpages/default.html', {'filter': c})


def user_list(request):
    f = F(request.GET, queryset=User.objects.all())
    return render(request, 'user_t.html', {'filter': f})


def product_list(request):
    c = C(request.GET, queryset=Product.objects.all())
    return render(request, 'product_t.html', {'filter': c})


def comment_list(request):
    x = X(request.GET, queryset=Comment.objects.all())
    return render(request, 'comment_t.html', {'filter': x})


class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'


# создаём представление в котором будет детали конкретного отдельного товара
class ProductDetail(DetailView):
    model = Product  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'flatpages/product_detail.html'  # название шаблона будет product.html
    context_object_name = 'product'  # название объекта. в нём будет


# дженерик для редактирования объекта
class ProductUpdateView(UpdateView):
    template_name = 'flatpages/product_create.html'
    model = Product
    fields = '__all__'
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)


# дженерик для удаления товара
class ProductDeleteView(DeleteView):
    template_name = 'flatpages/product_delete.html'
    model = Product
    success_url = '/products/'


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class ProductCreateView(CreateView):
    template_name = 'flatpages/product_create.html'
    form_class = ProductForm


