from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import FoodItem, Order, OrderItem, Profile


class FoodOrderBackendTests(TestCase):
    def setUp(self):
        self.food = FoodItem.objects.create(
            name="Test Pizza",
            description="Cheesy test pizza",
            category="Pizza",
            price=Decimal("199.00"),
            image_url="https://example.com/pizza.jpg",
            is_available=True,
        )
        self.user = User.objects.create_user(
            username="customer",
            password="pass12345",
            first_name="Test",
            last_name="Customer",
            email="customer@example.com",
        )
        self.user.profile.phone = "9876543210"
        self.user.profile.address = "Test address"
        self.user.profile.save()
        self.admin = User.objects.create_user(
            username="manager",
            password="pass12345",
            is_staff=True,
            email="manager@example.com",
        )

    def test_profile_is_created_for_new_users(self):
        user = User.objects.create_user(username="newuser", password="pass12345")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_public_pages_render(self):
        for name in ["home", "menu", "login", "register"]:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_register_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "Komal",
                "last_name": "Avhad",
                "username": "komal",
                "email": "komal@example.com",
                "phone": "9999999999",
                "address": "Pune",
                "password": "pass12345",
            },
        )

        self.assertRedirects(response, reverse("menu"))
        user = User.objects.get(username="komal")
        self.assertEqual(user.profile.phone, "9999999999")
        self.assertEqual(user.profile.address, "Pune")

    def test_login_redirects_customer_and_staff_correctly(self):
        response = self.client.post(reverse("login"), {"username": "customer", "password": "pass12345"})
        self.assertRedirects(response, reverse("menu"))

        self.client.logout()
        response = self.client.post(reverse("login"), {"username": "manager", "password": "pass12345"})
        self.assertRedirects(response, reverse("admin_dashboard"))

    def test_cart_checkout_creates_order_and_clears_cart(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("add_to_cart", args=[self.food.id]))
        self.assertRedirects(response, reverse("cart"))
        response = self.client.get(reverse("update_cart", args=[self.food.id, "increase"]))
        self.assertRedirects(response, reverse("cart"))

        response = self.client.post(reverse("checkout"))
        self.assertRedirects(response, reverse("menu"))

        order = Order.objects.get(user=self.user)
        item = OrderItem.objects.get(order=order)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(order.total_amount, Decimal("398.00"))
        self.assertEqual(self.client.session.get("cart"), {})

    def test_remove_and_decrease_cart_item(self):
        self.client.force_login(self.user)
        self.client.get(reverse("add_to_cart", args=[self.food.id]))
        self.client.get(reverse("update_cart", args=[self.food.id, "decrease"]))
        self.assertEqual(self.client.session.get("cart"), {})

        self.client.get(reverse("add_to_cart", args=[self.food.id]))
        self.client.get(reverse("remove_from_cart", args=[self.food.id]))
        self.assertEqual(self.client.session.get("cart"), {})

    def test_admin_pages_require_staff_and_render_for_staff(self):
        protected_names = [
            "admin_dashboard",
            "admin_add_food",
            "admin_manage_food",
            "admin_orders",
            "admin_users",
            "api_orders",
        ]

        for name in protected_names:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 302, name)

        self.client.force_login(self.admin)
        for name in protected_names:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)

    def test_admin_can_add_delete_food_and_update_order_status(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("admin_add_food"),
            {
                "name": "Test Burger",
                "price": "149.00",
                "category": "Burger",
                "image_url": "https://example.com/burger.jpg",
                "description": "Fresh burger",
                "is_available": "on",
            },
        )
        self.assertRedirects(response, reverse("admin_manage_food"))
        burger = FoodItem.objects.get(name="Test Burger")
        self.assertTrue(burger.is_available)

        order = Order.objects.create(user=self.user, total_amount=Decimal("199.00"))
        OrderItem.objects.create(order=order, food_item=self.food, quantity=1, price=self.food.price)
        response = self.client.post(reverse("admin_orders"), {"order_id": order.id, "status": "Delivered"})
        self.assertRedirects(response, reverse("admin_orders"))
        order.refresh_from_db()
        self.assertEqual(order.status, "Delivered")

        response = self.client.post(reverse("admin_delete_food", args=[burger.id]))
        self.assertRedirects(response, reverse("admin_manage_food"))
        self.assertFalse(FoodItem.objects.filter(id=burger.id).exists())

    def test_json_apis_return_serialized_data(self):
        response = self.client.get(reverse("api_foods"))
        self.assertEqual(response.status_code, 200)
        food_names = [food["name"] for food in response.json()["foods"]]
        self.assertIn("Test Pizza", food_names)

        order = Order.objects.create(user=self.user, total_amount=Decimal("199.00"))
        OrderItem.objects.create(order=order, food_item=self.food, quantity=1, price=self.food.price)

        self.client.force_login(self.admin)
        response = self.client.get(reverse("api_orders"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["orders"][0]["items"][0]["food"], "Test Pizza")
