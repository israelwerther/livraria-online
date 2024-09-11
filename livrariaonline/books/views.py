from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, View, FormView
from django.urls import reverse, reverse_lazy
from .models import Book, Cart, CartItem, Order, OrderItem
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView

class MyBooksListView(ListView):
    template_name = 'books/books.html'
    context_object_name = 'books'
    queryset = Book.objects.all()
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('books_list')

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


class CartListView(ListView):
    model = CartItem
    template_name = 'books/cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first()
        return cart.items.all() if cart else CartItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.save()
            session_key = self.request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()
        context['cart'] = cart
        return context


class CartItemRemoveView(View):
    template_name = 'books/cart.html'

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item_id')
        cart = get_object_or_404(Cart, session_key=request.session.session_key)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return redirect('cart')


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['next'] = reverse('order_success_redirect')
            request.session.modified = True
            return redirect(f'{reverse("login")}?next={request.session["next"]}')

        session_key = request.session.session_key
        cart = get_object_or_404(Cart, session_key=session_key)

        if cart.items.exists():
            order = Order.objects.create(user=request.user)
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity
                )
            cart.items.all().delete()
            request.session['order_id'] = order.id
            return redirect('order_success', order_id=order.id)
        else:
            return redirect('cart')


class OrderSuccessRedirectView(View):
    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id', None)
        if order_id:
            request.session['order_id'] = None
            return redirect(reverse('order_success', kwargs={'order_id': order_id}))
        else:
            return redirect(reverse('books_list'))


class OrderSuccessView(View):
    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'books/order_success.html', {'order': order})


class MyOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'books/my_orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def get_redirect_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('my_orders')

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.user.is_authenticated:
            session_key = self.request.session.session_key
            if session_key:
                cart = Cart.objects.filter(session_key=session_key).first()
                if cart:
                    cart.user = self.request.user
                    cart.session_key = None
                    cart.save()
        
        return response