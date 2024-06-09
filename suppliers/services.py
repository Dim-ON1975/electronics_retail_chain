from products.models import Product
from suppliers.models import ProductNetworkSupplier, NetworkSupplier


class SupplierService:
    """Сохранение поставки"""

    @staticmethod
    def save_supplier(serializer, product, request_user):
        # Создание и сохранение объекта NetworkSupplier
        network_supplier = serializer.save(author=request_user)

        # Создание и сохранение объекта ProductNetworkSupplier
        product_network_supplier = ProductNetworkSupplier.objects.create(network_supplier=network_supplier,
                                                                         product=product,
                                                                         author=request_user)
        product_network_supplier.save()


def find_suppliers_with_product(product: str, product_id: int) -> str:
    """
    Проверка наличия товаров у других поставщиков, если у текущего нет.
    :param product: Продукт, str.
    :param product_id: Идентификатор товара, int
    :return: Сообщение, str.
    """
    suppliers_with_product = NetworkSupplier.objects.filter(products=product)
    suppliers_list = ' | '.join([str(supplier) for supplier in suppliers_with_product])
    message_suppliers = (f"Вы можете создать новую поставку "
                         f"и выбрать '{product_id} - {product}' у одного из поставщиков: "
                         f"{suppliers_list}." if suppliers_list else "Ни у одного из поставщиков нет указанного товара.")
    return message_suppliers


def find_products_for_supplier(supplier: str) -> str:
    """
    Проверка наличия доступных товаров у выбранного поставщика
    :param supplier: Поставщик товара, str.
    :return: Сообщение, str.
    """
    product_with_supplier = Product.objects.filter(network_suppliers=supplier)
    products_list = ' | '.join([f'{product.id} - {str(product)}' for product in product_with_supplier])
    message_products = (f"Товары, доступные у выбранного поставщика: {products_list}."
                        if products_list else "У выбранного поставщика товаров нет.")
    return message_products


def check_product_existence(supplier: str, product_id: int, product: str) -> str:
    """
    Формирование сообщения об ошибке.
    :param supplier: Поставщик товара, str.
    :param product_id: Идентификатор товара, int
    :param product: Продукт, str
    :return: Сообщение об ошибке, str.
    """
    message_suppliers = find_suppliers_with_product(product, product_id)
    message_products = find_products_for_supplier(supplier)
    return f'У поставщика нет товара "{product_id} - {product}". {message_suppliers} {message_products}'


def check_product_ids(product_ids: list[int], update_supplier: bool = False) -> tuple[list[int], list[int]]:
    """
    Проверка и приведение к нужной форме id предаваемых продуктов
    :param product_ids: Идентификаторы продуктов, list[int, str, float]. Возможна передача данных любых типов
    :param update_supplier: Флаг, указывающий на то, что функция вызывается при изменении данных поставщика, bool.
    :return: Корректные идентификаторы продуктов, list[int].
    Если функция вызывается при изменении данных,
    то дополнительно возвращается список идентификаторов продуктов для удаления, list[int]
    """
    product_delete_ids = []
    if product_ids:
        # Оставляем только целые числа, если вдруг были переданы данные разных типов
        product_ids = [x for x in product_ids if isinstance(x, int)]

        if update_supplier:
            # Список продуктов поставщика на удаление (отрицательные целые числа)
            product_delete_ids = [abs(product_id) for product_id in product_ids if product_id < 0]

        # Избавляемся от отрицательных значений, исключаем ноль и дубликаты значений, сортируем по порядку
        product_ids = list(set([abs(product_id) for product_id in product_ids if product_id != 0]))
        product_ids.sort()

        # Получаем список всех имеющихся id продуктов из модели Product
        products_ids = Product.objects.values_list('id', flat=True)
        # Оставляем только те id, которые есть в Product, чтобы исключить ошибку, вызываемую несуществующим id
        product_ids = [prod_id for prod_id in product_ids if prod_id in products_ids]

    return product_ids, product_delete_ids
