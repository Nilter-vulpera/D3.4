from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFromToRangeFilter
from .models import Product, Category, Comment
from django.contrib.auth.models import User


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'quantity': ['gt'],
            'price': ['lt'],
            'category__name': ['contains'],
        }


class F(FilterSet):
    username = CharFilter(method='my_filter')

    class Meta:
        model = User
        fields = ['username']

    def my_filter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        }
                               )


class C(FilterSet):
    category = ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['category']


class X(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = Comment
        fields = ['date']
