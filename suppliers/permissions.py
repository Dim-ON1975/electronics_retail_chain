from rest_framework.permissions import BasePermission
from products.permissions import IsAdmin


class IsAuthor(BasePermission):
    """Права автора - доступ только к своему объекту"""
    message = 'Доступ запрещён, потому что Вы не являетесь автором.'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
