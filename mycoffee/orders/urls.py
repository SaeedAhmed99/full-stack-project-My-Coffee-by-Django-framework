from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:orderdetails_id>/', views.remove_to_cart, name='remove_to_cart'),
    path('cart/add_qty/<int:orderdetails_id>/', views.add_qty, name='add_qty'),
    path('cart/sub_qty/<int:orderdetails_id>/', views.sub_qty, name='sub_qty'),
]
