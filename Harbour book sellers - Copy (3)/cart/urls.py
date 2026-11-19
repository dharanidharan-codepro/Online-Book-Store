
from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='cart_add'),
    path('cart/update/<int:book_id>/', views.update_cart, name='cart_update'),
    path('cart/remove/<int:book_id>/', views.remove_from_cart, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/<str:order_number>/', views.success, name='success'),
    path('order/<str:order_number>/success/', views.success, name='order_success'),
]
