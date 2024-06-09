from django.urls import path

from .apps import SuppliersConfig
from .views import NetworkSupplierListCreateAPIView, NetworkSupplierRetrieveAPIView, NetworkSupplierUpdateAPIView, \
    NetworkSupplierDestroyAPIView

app_name = SuppliersConfig.name

urlpatterns = [
    path('supplier/', NetworkSupplierListCreateAPIView.as_view(), name='supplier-list-create'),
    path('supplier/<int:pk>/', NetworkSupplierRetrieveAPIView.as_view(), name='supplier-detail'),
    path('supplier/update/<int:pk>/', NetworkSupplierUpdateAPIView.as_view(), name='supplier-update'),
    path('supplier/delete/<int:pk>/', NetworkSupplierDestroyAPIView.as_view(), name='supplier-delete'),
]
