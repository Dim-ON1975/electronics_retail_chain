from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'phone', 'email', 'role', 'image', 'ad_big_image', 'is_active', 'date_joined',)
    readonly_fields = ('ad_image', 'ad_big_image',)
    list_display = ('email', 'id', 'ad_image', 'first_name', 'last_name', 'role', 'is_active', 'date_joined',)
    list_filter = ('last_name', 'email', 'role', 'is_active',)
    list_editable = ('role', 'is_active',)
    search_fields = ('first_name', 'last_name', 'email',)
    save_on_top = True

    @admin.display(description='Аватар', ordering='content')
    def ad_image(self, user: User):
        """
        Вычисляемое поле: отображение изображений в админ панели - маленькие изображения
        """
        if user.image:
            return mark_safe(f'<div style="width: 60px; height: 60px; '
                             f'border: 1px solid #C0C0C0; overflow: hidden">'
                             f'<img src="{user.image.url}" height=60 style:"margin: auto; display: block;"></div>')
        return 'Без фото'

    @admin.display(description='Аватар', ordering='content')
    def ad_big_image(self, user: User):
        """
        Вычисляемое поле: отображение изображений в админ панели - большие изображения
        """
        if user.image:
            return mark_safe(f'<div style="text-align: center; border: 1px solid #C0C0C0;">'
                             f'<img src="{user.image.url}" height=150></div>')
        return 'Без фото'


admin.site.unregister(Group)

admin.site.site_title = 'Админ-панель сайта сети продажи электроники'  # title админ-панели
admin.site.site_header = 'Админ-панель сайта сети продажи электроники'  # заголовок админ-панели
