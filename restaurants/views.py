from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages

from .forms import RestaurantRegistrationForm
from .models import Restaurant
from menu.models import MenuItem
from orders.models import Order
from reviews.models import Review


@login_required
def register_restaurant(request):
    # Auto-update role to restaurant owner if registering
    if request.user.role not in ["restaurant", "owner"] and not request.user.is_superuser:
        request.user.role = "restaurant"
        request.user.save()

    # Check if user already registered a restaurant
    existing = Restaurant.objects.filter(owner=request.user).first()
    if existing:
        messages.info(request, f"You have already registered '{existing.restaurant_name}'.")
        return redirect("restaurant_dashboard")

    if request.method == "POST":
        form = RestaurantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            # Instantly approve restaurant so customers can view it immediately!
            restaurant.status = "Approved"
            restaurant.save()

            messages.success(
                request,
                f"🎉 '{restaurant.restaurant_name}' registered successfully! It is now live and visible to customers."
            )
            return redirect("restaurant_dashboard")
        else:
            messages.error(request, "Please check the form fields and try again.")
    else:
        form = RestaurantRegistrationForm()

    return render(
        request,
        "restaurants/register_restaurant.html",
        {"form": form},
    )


@login_required
def edit_restaurant(request):
    restaurant = Restaurant.objects.filter(owner=request.user).first()
    if not restaurant and request.user.is_superuser:
        restaurant = Restaurant.objects.first()

    if not restaurant:
        messages.warning(request, "Please register your restaurant first.")
        return redirect("register_restaurant")

    if request.method == "POST":
        form = RestaurantRegistrationForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            rest = form.save(commit=False)
            rest.status = "Approved"
            rest.save()
            messages.success(request, "Restaurant details updated successfully!")
            return redirect("restaurant_dashboard")
    else:
        form = RestaurantRegistrationForm(instance=restaurant)

    return render(
        request,
        "restaurants/edit_restaurant.html",
        {"form": form, "restaurant": restaurant}
    )


@login_required
def restaurant_success(request):
    return render(request, "restaurants/restaurant_success.html")


@login_required
def restaurant_dashboard(request):
    restaurant = Restaurant.objects.filter(owner=request.user).first()
    if not restaurant and request.user.is_superuser:
        restaurant = Restaurant.objects.first()

    if not restaurant:
        messages.info(request, "No restaurant registered yet. Register your restaurant to get started!")
        return redirect("register_restaurant")

    orders = Order.objects.filter(restaurant=restaurant).order_by("-created_at")

    today = timezone.now().date()
    today_orders = orders.filter(created_at__date=today).count()
    pending_orders = orders.filter(status__in=["Pending", "Confirmed"]).count()
    completed_orders = orders.filter(status="Delivered").count()

    revenue = sum(
        order.total_amount
        for order in orders.filter(status="Delivered")
    )

    total_menu_items = MenuItem.objects.filter(restaurant=restaurant).count()
    recent_orders = orders[:10]
    popular_items = MenuItem.objects.filter(restaurant=restaurant, is_popular=True)
    latest_reviews = Review.objects.filter(restaurant=restaurant).order_by("-created_at")[:5]

    preparing_orders = orders.filter(status="Preparing").count()
    ready_orders = orders.filter(status="Ready for Pickup").count()
    delivery_orders = orders.filter(status="Out for Delivery").count()
    delivered_orders = completed_orders

    context = {
        "restaurant": restaurant,
        "today_orders": today_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "revenue": revenue,
        "total_menu_items": total_menu_items,
        "recent_orders": recent_orders,
        "popular_items": popular_items,
        "latest_reviews": latest_reviews,
        "preparing_orders": preparing_orders,
        "ready_orders": ready_orders,
        "delivery_orders": delivery_orders,
        "delivered_orders": delivered_orders,
    }

    return render(
        request,
        "restaurants/restaurant_dashboard.html",
        context,
    )


@login_required
def restaurant_orders(request):
    restaurant = Restaurant.objects.filter(owner=request.user).first()
    if not restaurant and request.user.is_superuser:
        restaurant = Restaurant.objects.first()

    if not restaurant:
        messages.warning(request, "Please register a restaurant first.")
        return redirect("register_restaurant")

    orders = Order.objects.filter(restaurant=restaurant).order_by("-created_at")

    status_filter = request.GET.get("status")
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(
        request,
        "restaurants/restaurant_orders.html",
        {"restaurant": restaurant, "orders": orders, "status_filter": status_filter}
    )


@login_required
def restaurant_reviews(request):
    restaurant = Restaurant.objects.filter(owner=request.user).first()
    if not restaurant and request.user.is_superuser:
        restaurant = Restaurant.objects.first()

    if not restaurant:
        messages.warning(request, "Please register a restaurant first.")
        return redirect("register_restaurant")

    reviews = Review.objects.filter(restaurant=restaurant).order_by("-created_at")

    return render(
        request,
        "restaurants/restaurant_reviews.html",
        {"restaurant": restaurant, "reviews": reviews}
    )


def restaurant_list(request):
    # Display all registered restaurants (approved or active)
    restaurants = Restaurant.objects.all().order_by('-created_at')

    search = request.GET.get("search")
    if search:
        restaurants = restaurants.filter(restaurant_name__icontains=search)

    cuisine = request.GET.get("cuisine")
    if cuisine:
        restaurants = restaurants.filter(cuisine__icontains=cuisine)

    return render(
        request,
        "restaurants/restaurant_list.html",
        {
            "restaurants": restaurants,
            "search": search,
            "cuisine": cuisine,
        },
    )


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    menu_items = MenuItem.objects.filter(
        restaurant=restaurant,
        is_available=True,
    )

    search = request.GET.get("search")
    if search:
        menu_items = menu_items.filter(food_name__icontains=search)

    category = request.GET.get("category")
    if category:
        menu_items = menu_items.filter(category__name=category)

    categories = menu_items.values_list("category__name", flat=True).distinct()
    reviews = Review.objects.filter(restaurant=restaurant).order_by("-created_at")[:10]

    return render(
        request,
        "restaurants/restaurant_detail.html",
        {
            "restaurant": restaurant,
            "menu_items": menu_items,
            "categories": categories,
            "reviews": reviews,
        },
    )