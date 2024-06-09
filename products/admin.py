from django.contrib import admin
from products.models import Product
from django.utils.safestring import mark_safe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель продуктов"""
    fields = ('owner', 'title', 'model', 'description', 'image', 'ad_big_image', 'release_date',)
    readonly_fields = ('ad_image', 'ad_big_image',)
    list_display = ('pk', 'owner', 'title', 'model', 'ad_image', 'release_date')
    list_filter = ('owner', 'title',)
    search_fields = ('owner', 'title', 'model', 'description')
    save_on_top = True

    @admin.display(description='Изображение', ordering='content')
    def ad_image(self, product: Product):
        """
        Вычисляемое поле: отображение изображений в админ панели - маленькие изображения
        """
        if product.image:
            return mark_safe(f'<div style="text-align: center; width: 60px; height: 60px; '
                             f'background-color: #DCDCDC; border: 1px solid #C0C0C0; overflow: hidden">'
                             f'<img src="{product.image.url}" height=60 style:"margin: auto; display: block;"></div>')
        return 'Без фото'

    @admin.display(description='Изображение', ordering='content')
    def ad_big_image(self, product: Product):
        """
        Вычисляемое поле: отображение изображений в админ панели - большие изображения
        """
        if product.image:
            return mark_safe(f'<p style="text-align: center"><img src="{product.image.url}" height=250></p>')
        return 'Без фото'
