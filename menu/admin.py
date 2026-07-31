from django.contrib import admin
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "food_name",
        "restaurant",
        "category",
        "price",
        "is_veg",
        "is_available",
        "is_popular",
    )

    list_filter = (
        "category",
        "is_veg",
        "is_available",
        "is_popular",
    )

    search_fields = (
        "food_name",
        "restaurant__restaurant_name",
    )