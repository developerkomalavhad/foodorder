from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import FoodItem, Order, OrderItem
from .serializers import serialize_food, serialize_order


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def get_cart(request):
    return request.session.setdefault("cart", {})


def home(request):
    featured_foods = FoodItem.objects.filter(is_available=True)[:6]
    return render(request, "home.html", {"featured_foods": featured_foods})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=request.POST.get("first_name", "").strip(),
                last_name=request.POST.get("last_name", "").strip(),
            )
            user.profile.phone = request.POST.get("phone", "").strip()
            user.profile.address = request.POST.get("address", "").strip()
            user.profile.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("menu")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )
        if user is not None:
            login(request, user)
            return redirect("admin_dashboard" if user.is_staff else "menu")
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


def menu(request):
    foods = FoodItem.objects.filter(is_available=True)
    return render(request, "menu.html", {"foods": foods})


@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id, is_available=True)
    cart = get_cart(request)
    item = cart.get(str(food.id), {"quantity": 0})
    item["quantity"] += 1
    cart[str(food.id)] = item
    request.session.modified = True
    messages.success(request, f"{food.name} added to cart.")
    return redirect("cart")


@login_required
def cart(request):
    cart_data = get_cart(request)
    food_ids = [int(food_id) for food_id in cart_data.keys()]
    foods = FoodItem.objects.filter(id__in=food_ids)
    cart_items = []
    total = Decimal("0.00")

    for food in foods:
        quantity = cart_data[str(food.id)]["quantity"]
        subtotal = food.price * quantity
        total += subtotal
        cart_items.append({"food": food, "quantity": quantity, "subtotal": subtotal})

    return render(request, "cart.html", {"cart_items": cart_items, "total": total})


@login_required
def update_cart(request, food_id, action):
    cart_data = get_cart(request)
    key = str(food_id)
    if key in cart_data:
        if action == "increase":
            cart_data[key]["quantity"] += 1
        elif action == "decrease":
            cart_data[key]["quantity"] -= 1
            if cart_data[key]["quantity"] <= 0:
                cart_data.pop(key)
        request.session.modified = True
    return redirect("cart")


@login_required
def remove_from_cart(request, food_id):
    cart_data = get_cart(request)
    cart_data.pop(str(food_id), None)
    request.session.modified = True
    return redirect("cart")


@login_required
@require_POST
def checkout(request):
    cart_data = get_cart(request)
    if not cart_data:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    foods = FoodItem.objects.filter(id__in=[int(food_id) for food_id in cart_data.keys()])
    total = Decimal("0.00")
    order = Order.objects.create(
        user=request.user,
        delivery_address=getattr(request.user, "profile", None).address if hasattr(request.user, "profile") else "",
    )

    for food in foods:
        quantity = cart_data[str(food.id)]["quantity"]
        total += food.price * quantity
        OrderItem.objects.create(order=order, food_item=food, quantity=quantity, price=food.price)

    order.total_amount = total
    order.save(update_fields=["total_amount"])
    request.session["cart"] = {}
    messages.success(request, f"Order #{order.id} placed successfully.")
    return redirect("menu")


@user_passes_test(is_staff_user)
def admin_dashboard(request):
    recent_orders = Order.objects.select_related("user").prefetch_related("items__food_item")[:5]
    revenue = Order.objects.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")
    context = {
        "total_orders": Order.objects.count(),
        "total_users": User.objects.filter(is_staff=False).count(),
        "food_count": FoodItem.objects.count(),
        "revenue": revenue,
        "recent_orders": recent_orders,
    }
    return render(request, "admin/dashboard.html", context)


@user_passes_test(is_staff_user)
def admin_add_food(request):
    if request.method == "POST":
        FoodItem.objects.create(
            name=request.POST.get("name", "").strip(),
            price=request.POST.get("price") or 0,
            category=request.POST.get("category", "Other"),
            image_url=request.POST.get("image_url", "").strip(),
            description=request.POST.get("description", "").strip(),
            is_available=request.POST.get("is_available") == "on",
        )
        messages.success(request, "Food item added.")
        return redirect("admin_manage_food")
    return render(request, "admin/add-food.html", {"categories": FoodItem.CATEGORY_CHOICES})


@user_passes_test(is_staff_user)
def admin_manage_food(request):
    foods = FoodItem.objects.all()
    return render(request, "admin/manage_food.html", {"foods": foods})


@user_passes_test(is_staff_user)
@require_POST
def admin_delete_food(request, food_id):
    get_object_or_404(FoodItem, pk=food_id).delete()
    messages.success(request, "Food item deleted.")
    return redirect("admin_manage_food")


@user_passes_test(is_staff_user)
def admin_orders(request):
    if request.method == "POST":
        order = get_object_or_404(Order, pk=request.POST.get("order_id"))
        order.status = request.POST.get("status", order.status)
        order.save(update_fields=["status"])
        messages.success(request, "Order status updated.")
        return redirect("admin_orders")
    orders = Order.objects.select_related("user").prefetch_related("items__food_item")
    return render(request, "admin/orders.html", {"orders": orders, "statuses": Order.STATUS_CHOICES})


@user_passes_test(is_staff_user)
def admin_users(request):
    users = User.objects.filter(is_staff=False).select_related("profile").order_by("id")
    return render(request, "admin/users.html", {"users": users})


def api_foods(request):
    foods = FoodItem.objects.all()
    return JsonResponse({"foods": [serialize_food(food) for food in foods]})


@user_passes_test(is_staff_user)
def api_orders(request):
    orders = Order.objects.prefetch_related("items__food_item").select_related("user")
    return JsonResponse({"orders": [serialize_order(order) for order in orders]})
