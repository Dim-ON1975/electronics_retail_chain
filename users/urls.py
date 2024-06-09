from django.urls import include, path, re_path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

users_router = SimpleRouter()

# Регистрируем ViewSet, который импортирован из приложения Djoser
users_router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(users_router.urls)),
    # аутентификация djoser
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),  # для работы с JWT
]
