from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:food_id>/<str:action>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:food_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-food/add/", views.admin_add_food, name="admin_add_food"),
    path("admin-food/manage/", views.admin_manage_food, name="admin_manage_food"),
    path("admin-food/delete/<int:food_id>/", views.admin_delete_food, name="admin_delete_food"),
    path("admin-orders/", views.admin_orders, name="admin_orders"),
    path("admin-users/", views.admin_users, name="admin_users"),
    path("api/foods/", views.api_foods, name="api_foods"),
    path("api/orders/", views.api_orders, name="api_orders"),
]
