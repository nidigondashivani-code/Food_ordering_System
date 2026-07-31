from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("voice-order/", views.voice_order_process, name="voice_order"),
    path("add/<int:menu_id>/", views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("remove/<int:item_id>/", views.remove_cart_item, name="remove_cart_item"),
    path("clear/", views.clear_cart, name="clear_cart"),
]
