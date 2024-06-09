from rest_framework import serializers
from products.models import Product
from users.serializers import CurrentUserSerializer


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор модели продукта. Позволяет добавлять сведения о создателе (владельце) продукта. """

    # Сведения о владельце (поле для сериализатора)
    owner = CurrentUserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
