from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('add-to-cart/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('cart/', views.cart_view, name='cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
