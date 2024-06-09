from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from products.models import Product


class ProductTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user@test.ru')
        self.user_admin = User.objects.create(email='user_admin@test.ru', role='admin')
        self.image = SimpleUploadedFile("test_ad.webp", b"file_content", content_type="image/webp")
        self.product = Product.objects.create(
            owner=self.user,
            title="title_product",
            model="model_product",
            description="description_product",
            image=self.image,
        )

        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user)

    def test_user(self):
        """ Тестирование роли пользователя """

        self.assertTrue(
            self.user.is_active,
            True
        )

        self.assertTrue(
            self.user.__str__(),
            "user@test.ru"
        )

        self.assertEqual(
            self.user.is_admin,
            False
        )

        self.assertEqual(
            self.user.is_staff,
            False
        )

        self.assertEqual(
            self.user.is_user,
            True
        )

        self.assertEqual(
            self.user.is_superuser,
            False
        )

        self.assertEqual(
            self.user is self.user.has_perm,
            False
        )

        self.assertEqual(
            self.user is self.user.has_module_perms,
            False
        )

    def test_create_product(self):
        """ Тестирование создания продукта """

        data = {
            "title": "title_product",
            "model": "model_product",
            "description": "description_product"
        }

        product_create_url = reverse('products:product-list')
        response = self.client.post(product_create_url, data=data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.json().get('action'),
            data.get('action')
        )

        self.assertTrue(
            Product.objects.get(pk=self.product.pk).title,
            data.get('action')
        )

        # Проверяем наличие записи в базе данных
        self.assertTrue(
            Product.objects.all().exists()
        )

        title = Product.objects.get(pk=self.product.pk).title
        model = Product.objects.get(pk=self.product.pk).model
        title_model = title + " - " + model
        self.assertEqual(
            title_model,
            str(self.product)
        )

    def test_list_product(self):
        """ Тестирование чтения списка продуктов """

        product_list_url = reverse('products:product-list')

        response = self.client.get(product_list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # self.assertEqual(
        #     Product.objects.get(pk=self.product.pk).title,
        #     response.json()[0].get('title'))

    def test_retrieve_product(self):
        """ Тест чтения одного продукта """

        product_one_url = reverse('products:product-detail', args=[self.product.pk])

        response = self.client.get(product_one_url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )

        response = response.json()

        self.assertEqual(response.get('owner')['id'], self.user.pk)
        self.assertEqual(response.get('title'), 'title_product')
        self.assertEqual(response.get('model'), 'model_product')
        self.assertEqual(response.get('description'), "description_product")

    def test_update_product(self):
        """ Тест редактирования продукта """

        data = {
            "title": "title_update_product",
            "model": "model_update_product",
            "description": "description_update_product"
        }

        product_update_url = reverse('products:product-detail', args=[self.product.pk])

        response = self.client.patch(product_update_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('owner')['id'], self.user.pk)
        self.assertEqual(response.get('title'), 'title_update_product')
        self.assertEqual(response.get('model'), 'model_update_product')
        self.assertEqual(response.get('description'), "description_update_product")

    def test_delete_product(self):
        """ Тест удаления продукта """

        product_delete_url = reverse('products:product-detail', args=[self.product.pk])

        response = self.client.delete(product_delete_url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Product.objects.all().exists(),
        )
