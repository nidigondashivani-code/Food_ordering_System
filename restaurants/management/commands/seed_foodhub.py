from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant
from menu.models import Category, MenuItem
from orders.models import Coupon
from datetime import time

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds initial database with foodhub sample restaurants, categories, menu items, coupons, and demo users."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. Create Users
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@foodhub.com", "role": "restaurant", "phone": "9998887770", "is_staff": True, "is_superuser": True}
        )
        admin_user.set_password("password123")
        admin_user.save()

        owner_user, _ = User.objects.get_or_create(
            username="owner1",
            defaults={"email": "owner@foodhub.com", "role": "restaurant", "phone": "9876543210"}
        )
        owner_user.set_password("password123")
        owner_user.save()

        delivery_user, _ = User.objects.get_or_create(
            username="delivery1",
            defaults={"email": "driver@foodhub.com", "role": "delivery", "phone": "9876543211"}
        )
        delivery_user.set_password("password123")
        delivery_user.save()

        customer_user, _ = User.objects.get_or_create(
            username="customer1",
            defaults={"email": "customer@foodhub.com", "role": "customer", "phone": "9876543212", "address": "123 Green Park Colony, Hyderabad"}
        )
        customer_user.set_password("password123")
        customer_user.save()

        self.stdout.write("Created demo users.")

        # 2. Categories
        cat_names = [
            "Biryani & North Indian",
            "Pizzas & Italian",
            "Burgers & Fast Food",
            "Asian & Noodles",
            "Desserts & Shakes"
        ]
        categories = {}
        for cname in cat_names:
            cat, _ = Category.objects.get_or_create(name=cname)
            categories[cname] = cat

        self.stdout.write("Created categories.")

        # 3. Restaurants
        restaurants_data = [
            {
                "name": "Paradise Biryani & Grill",
                "desc": "Authentic Hyderabadi Dum Biryani, Kebabs, and Mughlai delicacies prepared with royal spices.",
                "phone": "9876543201",
                "email": "paradise@foodhub.com",
                "address": "Banjara Hills, Road No 12",
                "city": "Hyderabad",
                "state": "Telangana",
                "pincode": "500034",
                "cuisine": "Hyderabadi / North Indian",
                "opening": time(10, 30),
                "closing": time(23, 0),
                "min_order": 150,
                "del_time": 30,
                "rating": 4.8,
                "status": "Approved",
            },
            {
                "name": "The Artisanal Pizza Oven",
                "desc": "Handcrafted wood-fired sourdough pizzas, fresh pasta, and gourmet garlic breads.",
                "phone": "9876543202",
                "email": "pizzaoven@foodhub.com",
                "address": "Jubilee Hills, Main Road",
                "city": "Hyderabad",
                "state": "Telangana",
                "pincode": "500033",
                "cuisine": "Italian / Pizza",
                "opening": time(11, 0),
                "closing": time(23, 30),
                "min_order": 200,
                "del_time": 25,
                "rating": 4.6,
                "status": "Approved",
            },
            {
                "name": "Urban Burger House",
                "desc": "Juicy smashed gourmet burgers, crispy loaded fries, and thick handcrafted ice cream shakes.",
                "phone": "9876543203",
                "email": "urbanburger@foodhub.com",
                "address": "Madhapur, Hitech City",
                "city": "Hyderabad",
                "state": "Telangana",
                "pincode": "500081",
                "cuisine": "American / Burgers",
                "opening": time(12, 0),
                "closing": time(2, 0),
                "min_order": 120,
                "del_time": 20,
                "rating": 4.5,
                "status": "Approved",
            },
            {
                "name": "Wok & Bowl Asian Kitchen",
                "desc": "Flavorful Dim Sums, Hakka Noodles, Spicy Ramen Bowls, and Thai Green Curry.",
                "phone": "9876543204",
                "email": "wokandbowl@foodhub.com",
                "address": "Gachibowli, Financial District",
                "city": "Hyderabad",
                "state": "Telangana",
                "pincode": "500032",
                "cuisine": "Pan-Asian / Chinese",
                "opening": time(11, 30),
                "closing": time(22, 30),
                "min_order": 180,
                "del_time": 35,
                "rating": 4.7,
                "status": "Approved",
            },
        ]

        restaurants = []
        for rdata in restaurants_data:
            rest, _ = Restaurant.objects.get_or_create(
                restaurant_name=rdata["name"],
                defaults={
                    "owner": owner_user,
                    "description": rdata["desc"],
                    "phone": rdata["phone"],
                    "email": rdata["email"],
                    "address": rdata["address"],
                    "city": rdata["city"],
                    "state": rdata["state"],
                    "pincode": rdata["pincode"],
                    "cuisine": rdata["cuisine"],
                    "opening_time": rdata["opening"],
                    "closing_time": rdata["closing"],
                    "minimum_order": rdata["min_order"],
                    "delivery_time": rdata["del_time"],
                    "rating": rdata["rating"],
                    "status": rdata["status"],
                }
            )
            restaurants.append(rest)

        self.stdout.write("Created restaurants.")

        # 4. Menu Items
        menu_items_data = [
            # Paradise Biryani
            {
                "restaurant": restaurants[0],
                "cat": categories["Biryani & North Indian"],
                "name": "Hyderabadi Mutton Dum Biryani",
                "desc": "Tender lamb marinated overnight in yoghurt and aromatic spices, layered with fragrant Basmati rice.",
                "price": 380,
                "cal": 650, "protein": 34.5, "carbs": 72.0, "fat": 22.0,
                "prep": 25, "is_veg": False, "popular": True
            },
            {
                "restaurant": restaurants[0],
                "cat": categories["Biryani & North Indian"],
                "name": "Special Paneer Butter Masala",
                "desc": "Soft cottage cheese cubes cooked in a rich, creamy tomato gravy topped with butter and kasuri methi.",
                "price": 280,
                "cal": 480, "protein": 18.0, "carbs": 24.0, "fat": 32.0,
                "prep": 20, "is_veg": True, "popular": True
            },
            {
                "restaurant": restaurants[0],
                "cat": categories["Biryani & North Indian"],
                "name": "Chicken Tangdi Kebab (4 pcs)",
                "desc": "Succulent chicken drumsticks coated in Tandoori marinade and grilled over glowing charcoal.",
                "price": 320,
                "cal": 420, "protein": 40.0, "carbs": 8.0, "fat": 16.0,
                "prep": 20, "is_veg": False, "popular": False
            },
            {
                "restaurant": restaurants[0],
                "cat": categories["Biryani & North Indian"],
                "name": "Garlic Butter Naan",
                "desc": "Fresh tandoori naan baked with roasted garlic bits and brushed with pure desi ghee.",
                "price": 60,
                "cal": 210, "protein": 6.0, "carbs": 38.0, "fat": 8.0,
                "prep": 10, "is_veg": True, "popular": True
            },

            # Pizza Oven
            {
                "restaurant": restaurants[1],
                "cat": categories["Pizzas & Italian"],
                "name": "Truffle Mushroom & Mozzarella Pizza",
                "desc": "Wood-fired crust with black truffle oil, wild mushrooms, fresh mozzarella, and fresh basil leaves.",
                "price": 490,
                "cal": 720, "protein": 24.0, "carbs": 85.0, "fat": 28.0,
                "prep": 20, "is_veg": True, "popular": True
            },
            {
                "restaurant": restaurants[1],
                "cat": categories["Pizzas & Italian"],
                "name": "Smoked Chicken Pepperoni Supreme Pizza",
                "desc": "Loaded with double smoked chicken pepperoni, roasted red bell peppers, and melted provolone.",
                "price": 540,
                "cal": 810, "protein": 36.0, "carbs": 88.0, "fat": 34.0,
                "prep": 22, "is_veg": False, "popular": True
            },
            {
                "restaurant": restaurants[1],
                "cat": categories["Pizzas & Italian"],
                "name": "Cheesy Garlic Breadsticks",
                "desc": "Crispy outside, soft inside breadsticks smothered in herb butter and three-cheese blend.",
                "price": 190,
                "cal": 350, "protein": 12.0, "carbs": 42.0, "fat": 16.0,
                "prep": 15, "is_veg": True, "popular": False
            },

            # Urban Burger House
            {
                "restaurant": restaurants[2],
                "cat": categories["Burgers & Fast Food"],
                "name": "Double Smash Bacon Cheeseburger",
                "desc": "Two smashed beef/chicken patties, crispy bacon strips, double cheddar cheese, and signature secret sauce.",
                "price": 320,
                "cal": 780, "protein": 42.0, "carbs": 48.0, "fat": 38.0,
                "prep": 15, "is_veg": False, "popular": True
            },
            {
                "restaurant": restaurants[2],
                "cat": categories["Burgers & Fast Food"],
                "name": "Crispy Mushroom & Avocado Veggie Burger",
                "desc": "Golden fried portobello mushroom patty topped with fresh sliced avocado, jalapeno mayo, and butter lettuce.",
                "price": 270,
                "cal": 520, "protein": 16.0, "carbs": 58.0, "fat": 22.0,
                "prep": 15, "is_veg": True, "popular": True
            },
            {
                "restaurant": restaurants[2],
                "cat": categories["Burgers & Fast Food"],
                "name": "Peri Peri Loaded Fries",
                "desc": "Crispy skin-on fries tossed in hot peri peri spice, drizzled with liquid cheese sauce and green onions.",
                "price": 160,
                "cal": 410, "protein": 7.0, "carbs": 52.0, "fat": 19.0,
                "prep": 12, "is_veg": True, "popular": False
            },

            # Wok & Bowl
            {
                "restaurant": restaurants[3],
                "cat": categories["Asian & Noodles"],
                "name": "Schezwan Chicken Hakka Noodles",
                "desc": "Wok-tossed noodles with tender shredded chicken, crunchy capsicum, and spicy schezwan sauce.",
                "price": 260,
                "cal": 540, "protein": 28.0, "carbs": 68.0, "fat": 18.0,
                "prep": 18, "is_veg": False, "popular": True
            },
            {
                "restaurant": restaurants[3],
                "cat": categories["Asian & Noodles"],
                "name": "Steamed Veg Crystal Dim Sum (6 pcs)",
                "desc": "Translucent dumplings filled with finely chopped water chestnuts, brocolli, and shiitake mushrooms.",
                "price": 230,
                "cal": 220, "protein": 6.0, "carbs": 38.0, "fat": 4.0,
                "prep": 15, "is_veg": True, "popular": True
            },

            # Desserts
            {
                "restaurant": restaurants[2],
                "cat": categories["Desserts & Shakes"],
                "name": "Triple Chocolate Fudge Brownie Shake",
                "desc": "Thick milk shake blended with dark chocolate fudge brownies, vanilla bean ice cream, and whipped cream.",
                "price": 190,
                "cal": 490, "protein": 9.0, "carbs": 65.0, "fat": 21.0,
                "prep": 10, "is_veg": True, "popular": True
            },
            {
                "restaurant": restaurants[0],
                "cat": categories["Desserts & Shakes"],
                "name": "Saffron Matka Shahi Phirni",
                "desc": "Traditional Kashmiri rice pudding infused with saffron, green cardamom, and silver leaf.",
                "price": 140,
                "cal": 310, "protein": 7.0, "carbs": 44.0, "fat": 12.0,
                "prep": 5, "is_veg": True, "popular": False
            },
        ]

        for mitem in menu_items_data:
            MenuItem.objects.get_or_create(
                restaurant=mitem["restaurant"],
                food_name=mitem["name"],
                defaults={
                    "category": mitem["cat"],
                    "description": mitem["desc"],
                    "price": mitem["price"],
                    "calories": mitem["cal"],
                    "protein": mitem["protein"],
                    "carbs": mitem["carbs"],
                    "fat": mitem["fat"],
                    "preparation_time": mitem["prep"],
                    "is_veg": mitem["is_veg"],
                    "is_popular": mitem["popular"],
                    "is_available": True,
                }
            )

        self.stdout.write("Created menu items.")

        # 5. Coupons
        coupons_data = [
            {"code": "WELCOME50", "percent": 20, "max": 100, "min": 200},
            {"code": "FOODHUB100", "percent": 25, "max": 150, "min": 350},
            {"code": "SUPER20", "percent": 15, "max": 80, "min": 150},
        ]

        for cdata in coupons_data:
            Coupon.objects.get_or_create(
                code=cdata["code"],
                defaults={
                    "discount_percent": cdata["percent"],
                    "max_discount": cdata["max"],
                    "min_order_amount": cdata["min"],
                    "active": True
                }
            )

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
