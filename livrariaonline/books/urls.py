from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api import CartViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('', views.MyBooksListView.as_view(), name='books_list'),
    path('', include(router.urls)),
]
