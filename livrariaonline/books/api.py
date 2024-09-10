from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .models import Book
from django.shortcuts import get_object_or_404


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        return Cart.objects.none()

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity', 1)

        book = get_object_or_404(Book, id=book_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        cart_item.quantity = quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        book_id = request.data.get('book_id')

        cart_item = get_object_or_404(CartItem, cart=cart, book_id=book_id)
        cart_item.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
