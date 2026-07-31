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
    
    # Smart Meal Planner Fitness Goals
    daily_calorie_goal = models.PositiveIntegerField(default=2000)
    fitness_goal = models.CharField(
        max_length=20,
        choices=FITNESS_GOAL_CHOICES,
        default='weight_loss'
    )
    protein_target = models.PositiveIntegerField(default=60)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username