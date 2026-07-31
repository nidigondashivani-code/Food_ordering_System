from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('paypal/complete/', views.paypal_complete_order, name='paypal_complete'),
    path('api/check-new-orders/', views.check_new_orders, name='check_new_orders'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
    path('confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('tracking/<str:order_number>/', views.order_tracking, name='order_tracking'),
    path('history/', views.customer_orders, name='customer_orders'),
    path('invoice/<str:order_number>/', views.order_invoice, name='order_invoice'),
    path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('delivery/', views.delivery_dashboard, name='delivery_dashboard'),
]
