from django.contrib import admin
from .models import Cart, CartItem, Book

admin.site.register([Book, Cart, CartItem])