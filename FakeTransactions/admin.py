from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'created']
    list_filter = ['created', 'category']
    list_editable = ['price']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
