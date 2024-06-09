from users.serializers import CurrentUserSerializer
from .models import NetworkSupplier
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class NetworkSupplierSerializer(serializers.ModelSerializer):
    """ Сериализатор поставщика """
    # Сведения об авторе (поле для сериализатора)
    owner = CurrentUserSerializer(read_only=True)
    supplier = serializers.SlugRelatedField(slug_field='id', queryset=NetworkSupplier.objects.all(), allow_null=True)
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        """ Получение списка товаров создаваемого поставщика вместо их id """
        products_list = [f'{product.id}) {product.title} - {product.model}' for product in obj.products.all()]
        products_list.sort()
        return products_list

    def validate(self, attrs):
        """ Валидация типа организации "Завод", "ИП", "Сеть магазинов" """
        type_supplier = attrs.get('type_supplier')
        supplier = attrs.get('supplier')

        if type_supplier == 0 and supplier:
            raise ValidationError('Поставщик типа "Завод" не может иметь поставщика.')
        if type_supplier > 0 and not supplier:
            raise ValidationError('Если поставщик не "Завод", то он должен иметь поставщика.')

        return attrs

    class Meta:
        model = NetworkSupplier
        fields = '__all__'
