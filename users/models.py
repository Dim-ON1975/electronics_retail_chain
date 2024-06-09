from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    """
    Enum-класс для пользователя
    """
    ADMIN = 'admin', _('ADMIN')
    USER = 'user', _('USER')


class User(AbstractBaseUser):
    """
    Абстрактный базовый класс, реализующий полнофункциональную модель пользователя с
    разрешениями, соответствующие требованиям администратора.
    Требуется имя адрес электронной почты и пароль. Остальные поля являются необязательными.
    """

    username = None
    first_name = models.CharField(max_length=50, **NULLABLE, verbose_name='имя')
    last_name = models.CharField(max_length=50, **NULLABLE, verbose_name='фамилия')
    phone = PhoneNumberField(**NULLABLE, verbose_name='телефон')
    email = models.EmailField(max_length=255, unique=True, verbose_name='электронная почта')
    role = models.CharField(max_length=5,
                            choices=UserRoles.choices,
                            default=UserRoles.USER,
                            **NULLABLE,
                            verbose_name='роль')
    image = models.ImageField(upload_to='users/%Y/%m/%d/', **NULLABLE, verbose_name='аватар')

    date_joined = models.DateTimeField(default=timezone.now, verbose_name='дата регистрации')

    is_active = models.BooleanField(
        **NULLABLE,
        default=True,
        help_text=_(
            'Указывает, следует ли считать этого пользователя активным. '
            'Отмените выбор вместо удаления учетных записей.'
        ),
        verbose_name='активный'
    )

    # Переопределение менеджера модели пользователя
    objects = UserManager()

    # эта константа определяет поле для логина пользователя
    USERNAME_FIELD = 'email'

    # эта константа содержит список с полями,
    # которые необходимо заполнить при создании пользователя
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        """ Админ, если роль == 'admin' """
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        """ Обычный пользователь, если роль == 'user' """
        return self.role == UserRoles.USER

    @property
    def is_superuser(self):
        """
        Пользователь - суперюзер, если его роль == 'admin'
        """
        return self.is_admin

    @property
    def is_staff(self):
        """
        Пользователь - сотрудник, если его роль == 'admin'
        """
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """
        У пользователя есть определённые разрешения, если его роль == 'admin'
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        У пользователя есть разрешения на просмотр приложения app_label,
        если его роль == 'admin'
        """
        return self.is_admin
