from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from products.models import Product
from products.permissions import IsAdmin
from .permissions import IsAuthor
from .filters import NetworkSupplierFilter
from .models import NetworkSupplier, ProductNetworkSupplier
from .pagination import SupplierPagination
from .serializers import NetworkSupplierSerializer
from .services import SupplierService, check_product_existence, check_product_ids


class NetworkSupplierListCreateAPIView(generics.ListCreateAPIView):
    """Просмотр списка и создание поставщиков"""
    queryset = NetworkSupplier.objects.all()
    serializer_class = NetworkSupplierSerializer
    pagination_class = SupplierPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkSupplierFilter
    # Просмотр списка - все (в т.ч. неавторизованные), создание - авторизованные
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Метод, который выполняется при создании нового объекта NetworkSupplier.
        Проверяет условия перед сохранением объекта.
        :param serializer: Сериализатор, содержащий данные для создания объекта
        """
        supplier = serializer.validated_data.get('supplier')
        type_supplier = serializer.validated_data.get('type_supplier')
        product_ids = self.request.data.get('products')

        # Проверка и приведение к нужной форме id предаваемых продуктов
        product_ids = check_product_ids(product_ids)[0]

        # Проверяем выбран ли хотя бы один продукт
        if not product_ids:
            raise ValidationError('Не выбран ни один продукт')

        errors = []  # сообщения об ошибках

        for product_id in product_ids:
            product = Product.objects.get(pk=product_id)
            # Проверяем, существует ли выбранный товар (product) у родительского поставщика (supplier)
            if supplier is not None:
                if not supplier.products.filter(id=product_id).exists():
                    # Проверка передаваемых данных
                    errors.append(check_product_existence(supplier, product_id, product))
                else:
                    # Если товар найден у родительского поставщика, то сохраняем его
                    SupplierService.save_supplier(serializer, product, self.request.user)

            elif type_supplier == 0:
                # Если товар найден и мы создаём завод (уровень 0)
                SupplierService.save_supplier(serializer, product, self.request.user)

        # если найдены ошибки, то выводим их, ничего не сохраняя
        if errors:
            raise ValidationError(errors)


class NetworkSupplierRetrieveAPIView(generics.RetrieveAPIView):
    """
    Детализация поставщика.
    Просматривать может только аутентифицированный пользователь.
    """
    queryset = NetworkSupplier.objects.all()
    serializer_class = NetworkSupplierSerializer
    permission_classes = [IsAuthenticated]


class NetworkSupplierUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление поставщика.
    Изменить могут только аутентифицированные авторы (владельцы) или администратор.
    """
    queryset = NetworkSupplier.objects.all()
    serializer_class = NetworkSupplierSerializer
    permission_classes = [IsAuthenticated, IsAuthor | IsAdmin]

    def perform_update(self, serializer):
        """
        Метод, который выполняется при редактировании нового объекта NetworkSupplier.
        Проверяет условия перед сохранением объекта, удаляет позиции товаров у поставщика,
        помеченные к удалению (нужно передавать отрицательные значения id, например. [-3, -2].
        :param serializer: Сериализатор, содержащий данные для создания объекта
        """
        supplier = serializer.validated_data.get('supplier')
        type_supplier = serializer.validated_data.get('type_supplier')
        product_ids = self.request.data.get('products')
        # Проверка и приведение к нужной форме id предаваемых продуктов
        product_ids, product_delete_ids = check_product_ids(product_ids, True)

        # Получаем перечень продуктов, которые имеются уже у текущего поставщика
        network_supplier_id = self.kwargs.get('pk')  # Получаем идентификатор из URL
        current_products = ProductNetworkSupplier.objects.filter(network_supplier=network_supplier_id).values_list(
            'product',
            flat=True)
        # Список новых продуктов на добавление (нет у редактируемого поставщика)
        new_products_ids = [product_id for product_id in product_ids if product_id not in current_products]

        errors = []  # сообщения об ошибках

        for product_id in product_ids:
            product = Product.objects.get(pk=product_id)
            # Проверяем, существует ли выбранный товар (product) у родительского поставщика (supplier)
            if supplier is not None:
                if not supplier.products.filter(id=product_id).exists():
                    # Проверка передаваемых данных
                    errors.append(check_product_existence(supplier, product_id, product))
                else:
                    # Если товар есть в списке новых продуктов, то сохраняем его
                    if product_id in new_products_ids:
                        SupplierService.save_supplier(serializer, product, self.request.user)
            elif type_supplier == 0:
                # Если товар есть в списке новых продуктов, то сохраняем его (завод (уровень 0))
                if product_id in new_products_ids:
                    SupplierService.save_supplier(serializer, product, self.request.user)
        else:
            # Если список продуктов был передан пустой, то просто сохраняем всё, что передали
            serializer.save(author=self.request.user)

        # Удаляем продукты у текущего поставщика, помеченные на удаление.
        # Выбираем записи ProductNetworkSupplier для удаления
        products_to_delete = ProductNetworkSupplier.objects.filter(network_supplier=network_supplier_id,
                                                                   product__in=product_delete_ids)
        products_to_delete.delete()  # Удаление

        # если найдены ошибки, то выводим их
        if errors:
            raise ValidationError(errors)


class NetworkSupplierDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление поставщика.
    Удалить могут только аутентифицированные авторы (владельцы) или администратор.
    """
    queryset = NetworkSupplier.objects.all()
    permission_classes = [IsAuthenticated, IsAuthor | IsAdmin]

    def perform_destroy(self, instance):
        # Удаление цепочки поставщиков, идущих после удаляемого поставщика
        instance.delete_chain()
