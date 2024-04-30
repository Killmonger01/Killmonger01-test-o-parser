from django.urls import path
from .views import run_parse#, get_product_list, get_product_detail

urlpatterns = [
    path('v1/products/', run_parse),
    #path('v1/products/', get_product_list),
    #path('v1/products/<int:product_id>/', get_product_detail),
]