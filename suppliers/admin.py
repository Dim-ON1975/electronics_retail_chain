from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import NetworkSupplier, ProductNetworkSupplier
from django import forms


class ProductNetworkSupplierInlineForm(forms.ModelForm):
    class Meta:
        model = ProductNetworkSupplier
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        # отслеживаем наличие товара у поставщика и если его нет, то не позволяем сохранять форму,
        # выводя соответствующее сообщение, указывающее, у каких поставщиков есть выбранный товар
        # и какие товары есть для выбора у выбранного поставщика
        network_supplier = cleaned_data.get('network_supplier')
        product = cleaned_data.get('product')
        if network_supplier.supplier and network_supplier.supplier.type_supplier != 'Завод':
            suppliers_with_product = NetworkSupplier.objects.filter(supplier__products=product)
            products_of_supplier = network_supplier.supplier.products.all()

            if network_supplier.supplier and product not in network_supplier.supplier.products.all():
                # перечень поставщиков
                supplier_list = [str(supplier) for supplier in suppliers_with_product]
                if len(supplier_list):
                    message_supplier = (f"Вы можете создать новую поставку и выбрать данный товар "
                                        f"у одного из поставщиков: <br>"
                                        f"{' | '.join([str(supplier) for supplier in suppliers_with_product])}.")
                else:
                    message_supplier = "Ни у одного из поставщиков нет указанного товара."

                # перечень товаров у поставщика на уровень выше
                product_list = [str(product) for product in products_of_supplier]
                if len(product_list):
                    message_product = (f"Товары, доступные у выбранного поставщика:<br>"
                                       f"{' | '.join([str(product) for product in products_of_supplier])}.")
                else:
                    message_product = "У выбранного поставщика товаров нет."
                error_message = format_html(f"У выбранного вами поставщика нет данного товара.<br>"
                                            f"{message_supplier}<br>"
                                            f"{message_product}")
                self.add_error('product', error_message)
        return cleaned_data


class ProductNetworkSupplierInline(admin.TabularInline):
    model = ProductNetworkSupplier
    form = ProductNetworkSupplierInlineForm
    extra = 0


class NetworkSupplierAdminForm(forms.ModelForm):
    class Meta:
        model = NetworkSupplier
        fields = '__all__'

    def clean(self):
        """Проверяем создаваемого поставщика"""
        cleaned_data = super().clean()
        supplier = cleaned_data.get('supplier')
        level = cleaned_data.get('level')
        supplier_type = cleaned_data.get('type_supplier')

        # Проверяем условие, что у завода не может быть поставщика
        if supplier_type == 0 and supplier:
            self.add_error('supplier', 'Поставщик типа "Завод" не может иметь поставщика.')

        # Проверяем указанный уровень
        if supplier:
            parent_level = supplier.level
            if level != parent_level + 1:
                self.add_error('level', f"Уровень должен быть равен {parent_level + 1}")

        return cleaned_data


@admin.register(NetworkSupplier)
class NetworkSupplierAdmin(admin.ModelAdmin):
    inlines = [ProductNetworkSupplierInline]
    list_display = ('id', 'author', 'name', 'get_supplier_chain', 'level', 'country', 'city', 'supplier_link', 'debt')
    list_filter = ('name', 'type_supplier', 'country', 'city',)
    actions = ['clear_debt']
    form = NetworkSupplierAdminForm

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                f'<a href="/admin/suppliers/networksupplier/{obj.supplier.id}/change/">{obj.supplier.name}</a>')
        return None

    supplier_link.allow_tags = True
    supplier_link.short_description = 'Поставщик'

    def clear_debt(self, request, queryset):
        queryset.update(debt=0)

    clear_debt.short_description = 'Очистить задолженность у выбранных поставщиков'

    @admin.display(description='Цепочка поставщиков')
    def get_supplier_chain(self, obj):
        """Цепочка поставщиков для большей наглядности"""
        # Формируем список поставщиков
        suppliers = [obj.supplier]
        current_supplier = obj.supplier
        while current_supplier:
            # Вставляем текущего поставщика в начало списка
            suppliers.insert(0, current_supplier.supplier)
            # Присваиваем переменной current_supplier родителя текущего поставщика
            # для перемещения по иерархии поставщиков от текущего поставщика к его родителям.
            current_supplier = current_supplier.supplier

        supplier_links = []
        # Создаем список ссылок на поставщиков
        for supplier in suppliers:
            if supplier:
                # Формируем путь к поставщику в админке
                path = reverse('admin:suppliers_networksupplier_change', args=[supplier.id])
                name = supplier.name  # наименование поставщика
                # гиперссылки на поставщиков
                supplier_link = format_html(f'<a href="{path}">{name}</a>')
                supplier_links.append(supplier_link)

        # Объединяем ссылки и выводим их в html-формате
        return format_html(' → '.join(supplier_links))
