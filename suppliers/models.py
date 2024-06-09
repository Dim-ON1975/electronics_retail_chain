from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from products.models import Product
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class NetworkSupplier(models.Model):
    """Модель элемента сети"""
    LEVEL_CHOICES = (
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)
    name = models.CharField(max_length=255, verbose_name='название')
    email = models.EmailField(verbose_name='электронная почта')
    phone = PhoneNumberField(verbose_name='номер телефона')
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    street = models.CharField(max_length=255, verbose_name='улица', **NULLABLE)
    house_number = models.CharField(max_length=10, verbose_name='номер дома', **NULLABLE)
    products = models.ManyToManyField(Product, through='ProductNetworkSupplier', related_name='network_suppliers',
                                      verbose_name='продукты')
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, related_name='child_elements',
                                 verbose_name='поставщик')
    type_supplier = models.IntegerField(choices=LEVEL_CHOICES, default=0, verbose_name='тип поставщика')
    level = models.IntegerField(default=0, verbose_name='уровень', **NULLABLE)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='задолженность', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    def save(self, *args, **kwargs):
        """Сохранение поставщиков"""
        if self.type_supplier == 0:  # Если тип поставщика - завод
            self.level = 0  # Устанавливаем уровень "Завод"
        elif self.supplier:  # Если есть поставщик
            self.level = self.supplier.level + 1  # Устанавливаем уровень на единицу выше уровня поставщика
        else:
            # В случае, если нет поставщика, уровень остается таким же
            pass

        super(NetworkSupplier, self).save(*args, **kwargs)

    def delete_chain(self):
        """Удаление поставщиков"""
        # Получаем всех поставщиков, которые следуют за текущим поставщиком по цепочке
        suppliers_to_delete = NetworkSupplier.objects.filter(supplier=self)

        # Удаляем товары текущего поставщика у следующих по цепочке поставщиков и удаляем их
        for supplier in suppliers_to_delete:
            # Проверяем уровень поставщика
            if supplier.level > self.level:
                # Удаление связи между объектом supplier и товарами
                # для удаления всех товаров, связанных с поставщиком
                supplier.products.clear()
                # Рекурсивный вызов для удаления цепочки поставщиков
                supplier.delete_chain()

        self.delete()  # Удаляем текущего поставщика

    def __str__(self):
        return f'{self.name}, уровень: {self.level}'

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class ProductNetworkSupplier(models.Model):
    """Модель для установления связи многие ко многим между моделями Product и NetworkSupplier"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    network_supplier = models.ForeignKey(NetworkSupplier, on_delete=models.CASCADE, verbose_name='сетевой элемент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    def __str__(self):
        return f'{self.product}: поставщик {self.network_supplier}'

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
