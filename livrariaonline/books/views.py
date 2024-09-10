from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse
from .models import Book, Cart, CartItem
from django.core.paginator import Paginator

class MyBooksListView(LoginRequiredMixin, ListView):
    template_name = 'books/books.html'
    context_object_name = 'books'
    queryset = Book.objects.all()
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect(reverse('books_list'))
    
    def get_queryset(self):
        queryset = Book.objects.all()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(title__icontains=query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page')
        books = paginator.get_page(page)
        context['books'] = books
        return context

    
