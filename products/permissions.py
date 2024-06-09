from rest_framework.permissions import BasePermission
from users.models import UserRoles


class IsAdmin(BasePermission):
    """Права администратора - доступ ко всем объектам"""

    def has_permission(self, request, view):
        """Права доступа на уровне всего запроса (от клиента)"""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Права доступа на уровне отдельного объекта (данных, записи БД)"""
        return request.user.role == UserRoles.ADMIN


class IsOwner(BasePermission):
    """Права создателя (владельца) - доступ только к своему объекту"""
    message = 'Доступ запрещён, потому что Вы не являетесь владельцем.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
