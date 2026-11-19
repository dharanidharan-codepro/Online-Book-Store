
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('books/', views.book_list, name='books'),
    path('category/<slug:slug>/', views.category_page, name='category'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail_alias'),
    path('assistant/', views.assistant_page, name='assistant'),
    path('assistant/message/', views.assistant_message, name='assistant_message'),
    path('assistant/intro-seen/', views.intro_seen, name='intro_seen'),
    path('cookies/consent/', views.cookie_consent, name='cookie_consent'),
]
