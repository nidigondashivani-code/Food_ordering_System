from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant Owner'),
        ('delivery', 'Delivery Partner'),
    )

    FITNESS_GOAL_CHOICES = (
        ('weight_loss', 'Weight Loss (Calorie Deficit)'),
        ('maintenance', 'Maintain Weight & Balance'),
        ('weight_gain', 'Weight Gain & Muscle Mass'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )
    profile_image_url = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    
    # Smart Meal Planner Fitness Goals
    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    fitness_goal = models.CharField(
        max_length=20,
        choices=FITNESS_GOAL_CHOICES,
        default='weight_loss'
    )
    protein_target = models.PositiveIntegerField(default=60)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_profile_image_url(self):
        if self.profile_image_url and self.profile_image_url.strip():
            return self.profile_image_url.strip()
        if self.profile_image:
            img_str = str(self.profile_image)
            if img_str.startswith('http://') or img_str.startswith('https://') or img_str.startswith('data:'):
                return img_str
            try:
                return self.profile_image.url
            except Exception:
                pass
        name = self.first_name or self.username
        return f"https://ui-avatars.com/api/?name={name}&background=ff385c&color=ffffff&size=128"

    def __str__(self):
        return self.username