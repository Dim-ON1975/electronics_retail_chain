from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from products.models import Product
from products.pagination import ProductPagination
from users.models import User
from products.permissions import IsAdmin, IsOwner
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Набор представлений продукта"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_permissions(self):
        """Права доступа"""
        if self.action == 'retrieve':
            # Детальный просмотр продукта - доступен аутентифицированным пользователям (IsOwner, IsAdmin)
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            # Создание продукта - доступно аутентифицированным пользователям (IsOwner, IsAdmin)
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Изменение и удаление продуктов - доступно владельцам (IsOwner) или админам (IsAdmin)
            permission_classes = [IsAuthenticated, IsOwner | IsAdmin]
        else:
            # Просмотр списка продуктов доступен всем
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Создание продукта и установление владельца."""
        product = serializer.save()
        product.owner = get_object_or_404(User, id=self.request.user.id)
        product.save()
