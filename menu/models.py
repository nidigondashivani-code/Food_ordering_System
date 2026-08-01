from django.db import models
from restaurants.models import Restaurant


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu_items"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    food_name = models.CharField(max_length=200)

    description = models.TextField()

    image = models.ImageField(
        upload_to="menu_items/",
        blank=True,
        null=True
    )

    image_url = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    calories = models.PositiveIntegerField(default=0)

    protein = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0
    )

    carbs = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0
    )

    fat = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0
    )

    preparation_time = models.PositiveIntegerField(
        help_text="Minutes"
    )

    is_veg = models.BooleanField(default=True)

    is_available = models.BooleanField(default=True)

    is_popular = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_image_url(self):
        url_str = (self.image_url or '').strip()
        if url_str.startswith('http://') or url_str.startswith('https://') or url_str.startswith('data:'):
            return url_str
        if self.image:
            img_str = str(self.image)
            if img_str.startswith('http://') or img_str.startswith('https://') or img_str.startswith('data:'):
                return img_str
            try:
                return self.image.url
            except Exception:
                pass
        return "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&auto=format&fit=crop&q=80"

    def __str__(self):
        return self.food_name