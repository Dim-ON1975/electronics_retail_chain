from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Менеджер пользовательской модели пользователя, где адрес электронной почты является уникальным идентификатором
    для аутентификации вместо имен пользователей.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Создание и сохранение пользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создание и сохранение суперпользователя (администратора) с указанным адресом электронной почты и паролем.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 'admin')

        return self.create_user(email, password, **extra_fields)
