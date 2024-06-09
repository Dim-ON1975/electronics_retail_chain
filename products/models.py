from django.db import models
from django.utils import timezone
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """ Модель продукта """

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    title = models.CharField(max_length=255, verbose_name='название')
    model = models.CharField(max_length=255, verbose_name='модель')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', **NULLABLE, verbose_name='превью')
    release_date = models.DateTimeField(default=timezone.now, verbose_name='дата выхода на рынок')

    def __str__(self):
        return f'{self.title} - {self.model}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
