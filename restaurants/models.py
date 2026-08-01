from django.db import models
from django.conf import settings


class Restaurant(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="restaurants"
    )

    restaurant_name = models.CharField(max_length=150)

    description = models.TextField()

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    cuisine = models.CharField(max_length=100)

    opening_time = models.TimeField()

    closing_time = models.TimeField()

    minimum_order = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    delivery_time = models.PositiveIntegerField(
        help_text="Delivery time in minutes"
    )

    logo = models.ImageField(
        upload_to="restaurant/logo/",
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to="restaurant/cover/",
        blank=True,
        null=True
    )

    fssai_license = models.FileField(
        upload_to="restaurant/licenses/",
        blank=True,
        null=True
    )

    gst_number = models.CharField(
        max_length=30,
        blank=True
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_logo_url(self):
        if not self.logo:
            return None
        img_str = str(self.logo)
        if img_str.startswith('http://') or img_str.startswith('https://') or img_str.startswith('data:'):
            return img_str
        try:
            return self.logo.url
        except Exception:
            return None

    @property
    def get_cover_image_url(self):
        if not self.cover_image:
            return None
        img_str = str(self.cover_image)
        if img_str.startswith('http://') or img_str.startswith('https://') or img_str.startswith('data:'):
            return img_str
        try:
            return self.cover_image.url
        except Exception:
            return None

    def __str__(self):
        return self.restaurant_name