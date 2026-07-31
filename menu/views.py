from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MenuItem, Category
from restaurants.models import Restaurant
from .forms import MenuItemForm

DEFAULT_CATEGORIES = [
    "Biryani & Starters",
    "North Indian Curries",
    "South Indian Tiffins",
    "Pizzas & Italian",
    "Burgers & Fast Food",
    "Chinese & Pan-Asian",
    "Tandoori & Kebabs",
    "Rolls & Wraps",
    "Seafood Specialities",
    "Desserts & Sweets",
    "Beverages & Shakes",
    "Ice Creams",
    "Healthy & Salads",
    "Bakery & Cakes",
    "Breakfast & Brunch",
]


def ensure_default_categories():
    for name in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(name=name)


def meal_planner(request):
    ensure_default_categories()

    # User goals or defaults
    user = request.user
    default_calorie = getattr(user, 'daily_calorie_goal', 2000) if user.is_authenticated else 2000
    default_goal = getattr(user, 'fitness_goal', 'weight_loss') if user.is_authenticated else 'weight_loss'
    default_protein = getattr(user, 'protein_target', 60) if user.is_authenticated else 60

    calorie_goal = int(request.GET.get('calorie_goal') or request.POST.get('calorie_goal') or default_calorie)
    fitness_goal = (request.GET.get('fitness_goal') or request.POST.get('fitness_goal') or default_goal).strip()
    protein_target = int(request.GET.get('protein_target') or request.POST.get('protein_target') or default_protein)

    # Save to user profile if submitted
    if request.method == "POST" and user.is_authenticated:
        user.daily_calorie_goal = calorie_goal
        user.fitness_goal = fitness_goal
        user.protein_target = protein_target
        user.save()
        messages.success(request, "🎯 Your Smart Meal Planner goals updated successfully!")

    items = MenuItem.objects.select_related("restaurant", "category").filter(is_available=True)

    # Filter items according to goal
    if fitness_goal == 'weight_loss':
        planner_items = items.filter(calories__lt=450).order_by('-protein', 'calories')
    elif fitness_goal == 'weight_gain':
        planner_items = items.filter(calories__gte=400).order_by('-calories', '-protein')
    else:
        planner_items = items.order_by('calories')

    # Group into Breakfast, Lunch, Snack, Dinner
    breakfast_items = planner_items.filter(category__name__icontains='Breakfast')[:3]
    if not breakfast_items.exists():
        breakfast_items = planner_items[:3]

    lunch_items = planner_items.filter(category__name__icontains='Indian')[:3]
    if not lunch_items.exists():
        lunch_items = planner_items[1:4]

    snack_items = planner_items.filter(category__name__icontains='Healthy')[:3]
    if not snack_items.exists():
        snack_items = planner_items[2:5]

    dinner_items = planner_items.filter(category__name__icontains='Tandoori')[:3]
    if not dinner_items.exists():
        dinner_items = planner_items[3:6]

    # Select top 1 meal from each for default full day plan calculation
    sample_plan = [
        breakfast_items.first(),
        lunch_items.first(),
        snack_items.first(),
        dinner_items.first()
    ]
    sample_plan = [item for item in sample_plan if item is not None]

    total_plan_calories = sum(item.calories for item in sample_plan)
    total_plan_protein = sum(item.protein for item in sample_plan)
    total_plan_price = sum(item.price for item in sample_plan)

    context = {
        'calorie_goal': calorie_goal,
        'fitness_goal': fitness_goal,
        'protein_target': protein_target,
        'breakfast_items': breakfast_items,
        'lunch_items': lunch_items,
        'snack_items': snack_items,
        'dinner_items': dinner_items,
        'sample_plan': sample_plan,
        'total_plan_calories': total_plan_calories,
        'total_plan_protein': total_plan_protein,
        'total_plan_price': round(total_plan_price, 2),
    }
    return render(request, 'menu/meal_planner.html', context)


def healthy_menu(request):
    ensure_default_categories()
    items = MenuItem.objects.select_related("restaurant", "category").filter(is_available=True)

    filter_type = request.GET.get("filter", "all")
    if filter_type == "low_calorie":
        items = items.filter(calories__lt=400)
    elif filter_type == "high_protein":
        items = items.filter(protein__gte=20)
    elif filter_type == "low_carb":
        items = items.filter(carbs__lt=30)
    elif filter_type == "veg":
        items = items.filter(is_veg=True)
    else:
        items = items.filter(calories__lt=500)

    context = {
        "menu_items": items.order_by("calories"),
        "filter_type": filter_type,
    }
    return render(request, "menu/healthy_menu.html", context)


def menu_list(request):
    ensure_default_categories()
    items = MenuItem.objects.select_related("restaurant", "category").filter(is_available=True)
    categories = Category.objects.all().order_by("name")

    search = request.GET.get("search")
    if search:
        items = items.filter(food_name__icontains=search)

    category = request.GET.get("category")
    if category:
        items = items.filter(category__name=category)

    calories = request.GET.get("calories")
    if calories == "low":
        items = items.filter(calories__lt=300)
    elif calories == "medium":
        items = items.filter(calories__range=(300, 500))
    elif calories == "high":
        items = items.filter(calories__gt=500)

    sort = request.GET.get("sort")
    if sort == "price_low":
        items = items.order_by("price")
    elif sort == "price_high":
        items = items.order_by("-price")

    context = {
        "menu_items": items,
        "categories": categories,
    }

    return render(request, "menu/restaurant_menu.html", context)


def get_user_restaurant(request):
    restaurant = Restaurant.objects.filter(owner=request.user).first()
    if not restaurant and request.user.is_superuser:
        restaurant = Restaurant.objects.first()
    return restaurant


@login_required
def add_menu_item(request):
    ensure_default_categories()
    restaurant = get_user_restaurant(request)
    if not restaurant:
        messages.warning(request, "Please register a restaurant before adding menu items.")
        return redirect("register_restaurant")

    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, f"🎉 '{menu_item.food_name}' added to your menu!")
            return redirect("restaurant_menu")
        else:
            messages.error(request, "Please check the form fields and try again.")
    else:
        form = MenuItemForm()

    return render(
        request,
        "menu/add_menu_item.html",
        {
            "form": form,
            "restaurant": restaurant,
        }
    )


@login_required
def restaurant_menu(request):
    ensure_default_categories()
    restaurant = get_user_restaurant(request)
    if not restaurant:
        messages.warning(request, "Please register a restaurant first.")
        return redirect("register_restaurant")

    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    search = request.GET.get("search")
    if search:
        menu_items = menu_items.filter(food_name__icontains=search)

    category = request.GET.get("category")
    if category:
        menu_items = menu_items.filter(category__name=category)

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "menu/restaurant_menu.html",
        {
            "menu_items": menu_items,
            "categories": categories,
            "restaurant": restaurant,
        },
    )


@login_required
def edit_menu_item(request, pk):
    ensure_default_categories()
    item = get_object_or_404(MenuItem, pk=pk)
    if not request.user.is_superuser and item.restaurant.owner != request.user:
        messages.error(request, "Permission denied.")
        return redirect("restaurant_menu")

    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated '{item.food_name}' successfully!")
            return redirect("restaurant_menu")
    else:
        form = MenuItemForm(instance=item)

    return render(request, "menu/edit_menu_item.html", {"form": form, "item": item})


@login_required
def delete_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if not request.user.is_superuser and item.restaurant.owner != request.user:
        messages.error(request, "Permission denied.")
        return redirect("restaurant_menu")

    item_name = item.food_name
    item.delete()
    messages.info(request, f"Deleted '{item_name}' from menu.")
    return redirect("restaurant_menu")