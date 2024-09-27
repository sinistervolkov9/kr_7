from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать привычки только владельцу.
    Публичные привычки доступны только для чтения другим пользователям.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешены только безопасные методы (GET, OPTIONS, HEAD)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Доступ на запись только владельцу привычки
        return obj.user == request.user
