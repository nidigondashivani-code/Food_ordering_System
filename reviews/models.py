from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from restaurants.models import Restaurant
from orders.models import Order


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="review",
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate average rating of restaurant
        all_reviews = Review.objects.filter(restaurant=self.restaurant)
        if all_reviews.exists():
            avg_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
            self.restaurant.rating = round(avg_rating, 1)
            self.restaurant.save()

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.restaurant_name} ({self.rating}★)"
