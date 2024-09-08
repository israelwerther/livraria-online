from django.urls import path
from .views import book_list_view

urlpatterns = [
    path('want-to-read/', book_list_view, name='book_list'),
]
