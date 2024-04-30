from django.contrib import admin

from .models import Product
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'image', 'price', 'discount',)
    search_fields = ('name',)
    empty_value_display = "-пусто-"