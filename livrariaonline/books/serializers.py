from rest_framework import serializers
from .models import Cart, CartItem
from .models import Book  # Importar o modelo Book

# Serializer para os itens do carrinho
class CartItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    book_price = serializers.DecimalField(source='book.price', max_digits=10, decimal_places=2, read_only=True)
    book_cover_url = serializers.CharField(source='book.cover_url', read_only=True)

    class Meta:
        model = CartItem
        fields = ['book', 'book_title', 'book_author', 'book_price', 'book_cover_url', 'quantity']

# Serializer para o carrinho
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_items']
