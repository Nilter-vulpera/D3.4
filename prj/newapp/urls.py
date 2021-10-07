from django.urls import path
from .views import ProductList, user_list, product_list, comment_list, Default, ProductList, ProductDetail, \
    ProductDeleteView, ProductCreateView,ProductUpdateView
from django.conf.urls import url

urlpatterns = [
    path('', ProductList.as_view()),
    url(r'^user_list/', user_list),
    path('product_list/', product_list),
    path('comment_list/', comment_list),
    path('news/', Default),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('create/', ProductCreateView.as_view(), name='product_create'),  # Ссылка на создание товара
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),

]
