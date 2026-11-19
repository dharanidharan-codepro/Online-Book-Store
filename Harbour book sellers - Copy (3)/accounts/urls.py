
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
