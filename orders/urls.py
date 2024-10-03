from django.urls import path
from . import views

app_name = 'add_to_cart'

urlpatterns=[
    path('add_to_cart',views.add_to_cart,name='add_to_cart'),
    path('cart',views.cart,name='cart'),
    path('<int:orderdetails_id>',views.remove_from_cart,name='remove_from_cart'),
]