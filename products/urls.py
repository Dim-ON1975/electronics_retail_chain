from django.urls import path
from products.apps import ProductsConfig
from products.views import ProductViewSet

app_name = ProductsConfig.name

# Связываем класс ProductViewSet с набором конкретных представлений
product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
]
