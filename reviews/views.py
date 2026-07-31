from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from .models import Review


@login_required
def add_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if hasattr(order, 'review') and order.review:
        messages.warning(request, "You have already submitted a review for this order.")
        return redirect('customer_orders')

    if request.method == "POST":
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()

        if rating < 1 or rating > 5:
            messages.error(request, "Rating must be between 1 and 5 stars.")
            return redirect('add_review', order_id=order_id)

        Review.objects.create(
            user=request.user,
            restaurant=order.restaurant,
            order=order,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Thank you for your review!")
        return redirect('customer_orders')

    return render(request, 'reviews/add_review.html', {'order': order})
