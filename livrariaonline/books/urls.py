from django.urls import path, include
from . import views

# router = DefaultRouter()
# router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('', views.MyBooksListView.as_view(), name='books_list'),
    path('cart/', views.CartListView.as_view(), name='cart'),
    path('cart/remove/', views.CartItemRemoveView.as_view(), name='cart_remove'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.MyOrdersListView.as_view(), name='my_orders'),  # URL para a página de compras realizadas
    path('order/complete/<int:order_id>/', views.OrderSuccessView.as_view(), name='order_success'),
    path('order/success-redirect/', views.OrderSuccessRedirectView.as_view(), name='order_success_redirect'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]
