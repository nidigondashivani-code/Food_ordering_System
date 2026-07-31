import uuid
from django.db import models
from django.conf import settings
from restaurants.models import Restaurant
from menu.models import MenuItem


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    max_discount = models.DecimalField(max_digits=8, decimal_places=2, default=100)
    min_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    valid_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% off)"

    def calculate_discount(self, subtotal):
        subtotal_val = float(subtotal)
        min_amount_val = float(self.min_order_amount)
        if subtotal_val < min_amount_val:
            return 0.0
        discount = (subtotal_val * float(self.discount_percent)) / 100.0
        return min(discount, float(self.max_discount))



class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Preparing', 'Preparing'),
        ('Ready for Pickup', 'Ready for Pickup'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI Payment'),
        ('Card', 'Credit/Debit Card'),
        ('NetBanking', 'Net Banking'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    )

    order_number = models.CharField(max_length=50, unique=True, editable=False)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    delivery_partner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='delivery_orders'
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    delivery_address = models.TextField()
    phone = models.CharField(max_length=20)
    special_notes = models.TextField(blank=True)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=40)
    tax_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_code = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"FH-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"

    @property
    def is_completed(self):
        return self.status == 'Delivered'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.SET_NULL,
        null=True
    )
    food_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.food_name} (Order {self.order.order_number})"

    @property
    def get_cost(self):
        return float(self.price * self.quantity)
