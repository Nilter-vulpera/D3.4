from django.urls import path
from .views import ProductList, user_list, product_list, comment_list
from django.conf.urls import url

urlpatterns = [
    path('', ProductList.as_view()),
    url(r'^user_list', user_list),
    path('product_list', product_list),
    path('comment_list', comment_list),
]
