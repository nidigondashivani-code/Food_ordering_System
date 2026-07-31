from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_list, name="menu"),
    path("planner/", views.meal_planner, name="meal_planner"),
    path("healthy/", views.healthy_menu, name="healthy_menu"),
    path("add/", views.add_menu_item, name="add_menu_item"),
    path("restaurant/", views.restaurant_menu, name="restaurant_menu"),
    path("edit/<int:pk>/", views.edit_menu_item, name="edit_menu_item"),
    path("delete/<int:pk>/", views.delete_menu_item, name="delete_menu_item"),
]