from djoser.serializers import UserSerializer as BaseUserSerializer, \
    UserCreateSerializer as BaseUserRegistrationSerializer, UserCreatePasswordRetypeSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    """ Сериализация регистрации пользователя """

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('first_name', 'last_name', 'phone', 'email', 'password')


class CurrentUserSerializer(BaseUserSerializer):
    """ Сериализация модели User. Отображение данных пользователя. """

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'image', 'role', 'date_joined', 'is_active',)


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    """ Сериализация повторной проверки пароля, вводимого пользователем """
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'password')
