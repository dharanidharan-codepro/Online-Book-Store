from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('category/<slug:category_slug>/', views.book_list, name='category'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('books/<slug:slug>/summary/', views.book_summary, name='book_summary'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/success/', views.order_success, name='order_success'),
]
