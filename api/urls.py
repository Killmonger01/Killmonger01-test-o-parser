from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import get_product_by_id, get_product_list, run_parse

schema_view = get_schema_view(
   openapi.Info(
      title="ozon_parse API",
      default_version='v1',
      description="ozon_parse API",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('v1/products/', run_parse, name='v1-products'),
   path('v1/get/products/', get_product_list, name='v1-get-products'),
   path('v1/get/products/<int:product_id>/', get_product_by_id, name='v1-get-product-by-id'),
]
