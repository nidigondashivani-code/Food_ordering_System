from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, OwnerRegisterForm
from restaurants.models import Restaurant
from menu.models import MenuItem, Category
from orders.models import Coupon


def home(request):
    featured_restaurants = Restaurant.objects.filter(status="Approved").order_by('-rating')[:6]
    categories = Category.objects.all()[:8]
    popular_items = MenuItem.objects.filter(is_available=True, is_popular=True)[:8]
    if not popular_items.exists():
        popular_items = MenuItem.objects.filter(is_available=True)[:8]
    active_coupons = Coupon.objects.filter(active=True)[:3]

    context = {
        'featured_restaurants': featured_restaurants,
        'categories': categories,
        'popular_items': popular_items,
        'active_coupons': active_coupons,
    }
    return render(request, 'home.html', context)


def owner_register(request):
    if request.method == "POST":
        form = OwnerRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "Restaurant Owner account registered successfully! Please login."
            )
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = OwnerRegisterForm()

    return render(
        request,
        "restaurant_owner_register.html",
        {"form": form},
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account registered successfully! Please login."
            )
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        if request.user.role in ["restaurant", "owner"]:
            return redirect("restaurant_dashboard")
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.first_name or user.username}!"
            )

            if user.role in ["restaurant", "owner"]:
                return redirect("restaurant_dashboard")
            elif user.role == "delivery":
                return redirect("delivery_dashboard")
            else:
                return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def user_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)
        user.profile_image_url = request.POST.get('profile_image_url', user.profile_image_url)

        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'users/profile.html')


@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get('confirm_password')
        user = request.user

        if not password or not user.check_password(password):
            messages.error(request, "Incorrect password. Account deletion cancelled.")
            return redirect('profile')

        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')

    return redirect('profile')