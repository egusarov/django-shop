from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("parent",)
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("category",)
    search_fields = ("name", "description")
    ordering = ("name",)
