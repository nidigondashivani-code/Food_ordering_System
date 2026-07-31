from django.test import TestCase
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant
from menu.models import MenuItem, Category
from orders.models import Order, OrderItem, Coupon
from datetime import time

User = get_user_model()


class FoodHubTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="testowner", password="password123", role="restaurant", phone="1111111111")
        self.customer = User.objects.create_user(username="testcustomer", password="password123", role="customer", phone="2222222222")

        self.restaurant = Restaurant.objects.create(
            owner=self.owner,
            restaurant_name="Test Cafe",
            description="Test cafe desc",
            phone="1111111111",
            email="cafe@test.com",
            address="123 Street",
            city="Hyderabad",
            state="Telangana",
            pincode="500001",
            cuisine="Indian",
            opening_time=time(9, 0),
            closing_time=time(22, 0),
            delivery_time=30,
            status="Approved"
        )

        self.category = Category.objects.create(name="Starters")
        self.menu_item = MenuItem.objects.create(
            restaurant=self.restaurant,
            category=self.category,
            food_name="Paneer Tikka",
            description="Spicy grilled paneer",
            price=250.00,
            preparation_time=15,
            is_available=True
        )

        self.coupon = Coupon.objects.create(
            code="TEST20",
            discount_percent=20,
            max_discount=100,
            min_order_amount=200,
            active=True
        )

    def test_coupon_discount_calculation(self):
        discount = self.coupon.calculate_discount(300)
        self.assertEqual(discount, 60.0)

    def test_order_creation(self):
        order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address="456 Park Road",
            phone="2222222222",
            subtotal=250.00,
            delivery_fee=40.00,
            tax_amount=12.50,
            discount_amount=0,
            total_amount=302.50,
            status="Confirmed"
        )
        self.assertTrue(order.order_number.startswith("FH-"))

        item = OrderItem.objects.create(
            order=order,
            menu_item=self.menu_item,
            food_name=self.menu_item.food_name,
            price=self.menu_item.price,
            quantity=2
        )
        self.assertEqual(item.get_cost, 500.00)
