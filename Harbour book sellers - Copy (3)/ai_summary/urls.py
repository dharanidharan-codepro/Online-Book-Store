
from django.urls import path
from . import views

urlpatterns = [
    path('summary/<slug:slug>/', views.summary_json, name='book_summary'),
    path('books/<slug:slug>/summary/', views.summary_json, name='book_summary_alias'),
]
