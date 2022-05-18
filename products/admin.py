from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'price', 'created', 'updated',)


admin.site.register(Product, ProductAdmin)
