from django.urls import reverse

from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from suppliers.models import NetworkSupplier, Product, ProductNetworkSupplier
from suppliers.serializers import NetworkSupplierSerializer
from suppliers.services import SupplierService, check_product_ids
from rest_framework.test import APITestCase


class NetworkSupplierTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', password='testpassword', role='admin')
        self.product = Product.objects.create(owner=self.user, title='Test Product', model='Test Model')
        self.client.force_authenticate(user=self.user)

    def test_network_supplier_operations(self):
        # Тестирование создания сетевого поставщика
        supplier1 = NetworkSupplier.objects.create(
            supplier=None,
            name='Supplier 1',
            email='suppl@test.ru',
            phone='+79198584502',
            type_supplier=0
        )
        supplier1.products.set([self.product.id])

        # Сохраняем поставщика supplier3 в базе данных
        supplier1.save()
        product_ids = [self.product.id]
        data_create = {
            "supplier": supplier1.id,
            "name": "Supplier Name",
            "email": "supplier@example.com",
            "phone": "+79285678945",
            "type_supplier": 1,
            "products": product_ids
        }
        supplier_create_url = reverse('suppliers:supplier-list-create')
        response_create = self.client.post(supplier_create_url, data_create, format='json')
        self.assertEqual(response_create.status_code, 201)

        # Тестирование удаления поставщика и цепочки поставок
        supplier2 = NetworkSupplier.objects.create(
            supplier=None,
            name='Supplier 2',
            email='suppl@test.ru',
            phone='+79198584502',
            type_supplier=0
        )
        supplier2.products.set([self.product.id])

        # Сохраняем поставщика supplier3 в базе данных
        supplier2.save()

        supplier2.products.set([self.product.id])
        product_network_supplier = ProductNetworkSupplier.objects.create(network_supplier=supplier2,
                                                                         product=self.product, author=self.user)
        supplier2.products.add(self.product)
        supplier2.delete_chain()
        self.assertFalse(NetworkSupplier.objects.filter(id=supplier2.id).exists())
        self.assertFalse(ProductNetworkSupplier.objects.filter(network_supplier=supplier2).exists())

    def test_supplier_service_save_supplier(self):
        """Тестирование функции сохранения поставщика"""
        supplier3 = NetworkSupplier.objects.create(
            supplier=None,
            name='Supplier 3',
            email='suppl@test.ru',
            phone='+79198584502',
            type_supplier=0
        )
        supplier3.products.set([self.product.id])

        # Сохраняем поставщика supplier3 в базе данных
        supplier3.save()

        serializer_data = {
            "supplier": supplier3.id,
            "name": "Supplier Name",
            "email": "supplier@example.com",
            "phone": "+79285678945",
            "type_supplier": 1,
            "products": [self.product.id]
        }

        serializer = NetworkSupplierSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        SupplierService.save_supplier(serializer, self.product, self.user)

        network_supplier = NetworkSupplier.objects.get(id=supplier3.id)
        product_network_supplier = ProductNetworkSupplier.objects.filter(network_supplier=network_supplier,
                                                                         product=self.product).first()

        self.assertIsNotNone(network_supplier)
        self.assertIsNotNone(product_network_supplier)

    def test_update_network_supplier(self):
        """Тестирование изменения поставщиков"""
        supplier4 = NetworkSupplier.objects.create(
            supplier=None,
            name='Supplier 4',
            email='suppl@test.ru',
            phone='+79198584502',
            type_supplier=0
        )
        supplier4.products.set([self.product.id])

        supplier4.save()
        products = [self.product.id]
        data = {
            "supplier": supplier4.id,
            "products": products,
            "name": "Тест",
            "email": "bukashka@test.ru",
            "phone": "+79594455244",
            "type_supplier": 1
        }
        url = reverse('suppliers:supplier-update', kwargs={'pk': supplier4.id})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)  # Проверка успешного обновления

        updated_supplier = NetworkSupplier.objects.get(id=supplier4.id)
        self.assertEqual(updated_supplier.id, 8)  # Проверка обновления имени

        # Проверка добавления новых продуктов
        self.assertTrue(updated_supplier.products.filter(id=self.product.id).exists())

        # Проверка добавления продуктов, которых нет у поставщика
        product1 = Product.objects.create(title='Product1', model="Model1")
        product2 = Product.objects.create(title='Product2', model="Model2")
        supplier5 = NetworkSupplier.objects.create(
            supplier=None,
            name='Supplier 5',
            email='suppl@test.ru',
            phone='+79198584502',
            type_supplier=0
        )
        supplier5.products.add(product1)
        supplier5.products.add(product2)
        supplier5.products.set([self.product.id, product1.id])

        # Сохраняем поставщика supplier3 в базе данных
        supplier5.save()
        products = [product1.id, product2.id]  # Новые продукты для добавления
        data = {
            "supplier": supplier5.id,
            "products": products,
            "name": "Тест",
            "email": "bukashka@test.ru",
            "phone": "+79594455244",
            "type_supplier": 1
        }
        url = reverse('suppliers:supplier-update', kwargs={'pk': supplier5.id})
        response = self.client.put(url, data, format='json')
        message = '["У поставщика нет товара "12 - Product2..."]'
        self.assertEqual(
            response.content.decode('utf-8')[:25],
            message[:25])
        self.assertEqual(response.status_code, 400)

    def test_retrieve_network_supplier(self):
        """Тестирование просмотра одного поставщика"""
        supplier = NetworkSupplier.objects.create(name='Supplier1', email='supplier1@example.com', phone='+79594455244',
                                                  type_supplier=1)
        url = reverse('suppliers:supplier-detail', kwargs={'pk': supplier.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)  # Проверка успешного получения информации о поставщике
        self.assertEqual(response.data['name'], 'Supplier1')  # Проверка корректности возвращаемых данных

    def test_destroy_network_supplier(self):
        """Тестирование удаления"""
        supplier = NetworkSupplier.objects.create(name='Supplier1', email='supplier1@example.com', phone='+79594455244',
                                                  type_supplier=1)
        url = reverse('suppliers:supplier-delete', kwargs={'pk': supplier.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)  # Проверка успешного удаления
        supplier_exists = NetworkSupplier.objects.filter(id=supplier.id).exists()
        self.assertFalse(supplier_exists)  # Проверка отсутствия поставщика после удаления

    def test_check_product_ids(self):
        """Тестирование проверки передаваемого списка id продуктов"""

        # При создании поставщика
        product_ids = [1, 2, 3, 8, 11, 12, 0.5, 2.6, 'a', 'b', 'c', -5, -6]
        product_ids_create = check_product_ids(product_ids)[0]
        self.assertEqual(product_ids_create, [8])

        # При изменении поставщика
        product_ids = [1, 2, 3, 8, 11, 12, 0.5, 2.6, 'a', 'b', 'c', -5, -6]
        product_ids_update, product_delete_ids_update = check_product_ids(product_ids, True)
        self.assertEqual(product_ids_update, [8])
        self.assertEqual(product_delete_ids_update, [5, 6])

        # Пустой список
        product_ids = []
        product_ids_update, product_delete_ids_update = check_product_ids(product_ids, True)
        self.assertEqual(product_ids_update, [])
        self.assertEqual(product_delete_ids_update, [])
