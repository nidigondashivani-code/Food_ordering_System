from django.db import models
from django.conf import settings
from menu.models import MenuItem


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cart"
    )
    session_key = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart ({self.user.username})"
        return f"Cart ({self.session_key})"

    @property
    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def get_subtotal(self):
        return float(sum(item.get_cost for item in self.items.all()))

    @property
    def get_restaurant(self):
        first_item = self.items.first()
        if first_item and first_item.menu_item:
            return first_item.menu_item.restaurant
        return None


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.food_name}"

    @property
    def get_cost(self):
        return float(self.menu_item.price * self.quantity)
