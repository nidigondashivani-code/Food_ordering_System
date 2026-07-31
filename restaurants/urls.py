from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.restaurant_list, name="restaurant_list"),
    path("register/", views.register_restaurant, name="register_restaurant"),
    path("edit/", views.edit_restaurant, name="edit_restaurant"),
    path("dashboard/", views.restaurant_dashboard, name="restaurant_dashboard"),
    path("orders/", views.restaurant_orders, name="restaurant_orders"),
    path("reviews/", views.restaurant_reviews, name="restaurant_reviews"),
    path("success/", views.restaurant_success, name="restaurant_success"),
    path("<int:restaurant_id>/", views.restaurant_detail, name="restaurant_detail"),
]