from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger, redoc
schema_view = get_schema_view(
    openapi.Info(
        title="API документация",
        default_version='v1',
        description="Проект \"Сеть по продаже электроники\"",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="zaberov.dv@internet.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # админка
    path("admin/", admin.site.urls),
    # приложения
    path('', include('users.urls'), name='user'),
    path('', include('products.urls', namespace='products')),
    path('', include('suppliers.urls', namespace='suppliers')),
    # документация (swagger, redoc, specicular)
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
