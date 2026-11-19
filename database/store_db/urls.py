
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-to-cart/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_history, name="order_history"),
    path("add-book/", views.add_book, name="add_book"),
]
