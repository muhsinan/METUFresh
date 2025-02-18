from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("", views.main_view, name="main"),
    path("", views.navbar_view, name="navbar"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("cart/", views.cart_view, name="cart"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("product/<str:pk>/", views.product_view, name="product"),
    path("create-product/", views.create_product, name="create-product"),
    path("update-product/<str:pk>/", views.update_product, name="update-product"),
    path("delete-product/<str:pk>/", views.delete_product, name="delete-product"),
    path("search/", views.search_view, name="search"),
]
