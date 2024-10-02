from django.shortcuts import render,redirect
from django.contrib import messages
from products.models import Product
from .models import Order,OrderDetails
from django.utils import timezone

def add_to_cart(request):

    if 'pro_id' in request.GET and 'price' in request.GET and 'qty' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:

        # order=Order.objects.create(user=request.user,order_date=timezone.now,is_finished=False)
        pro_id=request.GET['pro_id']
        qty=request.GET['qty']

        order=Order.objects.filter(user=request.user,is_finished=False)

        if not Product.objects.all().filter(pk=pro_id).exists():
            return redirect('products:products')
        
        pro=Product.objects.get(pk=pro_id)

        if order:
            old_order=Order.objects.get(user=request.user,is_finished=False)

            orderDetails=OrderDetails.objects.create(order=old_order,product=pro,price=pro.price,quantity=qty)
            messages.success(request,'Was added to cart for old order')


        else:
            new_order=Order.objects.create(user=request.user,order_date=timezone.now(),is_finished=False)
            OrderDetails.objects.create(order=new_order,product=pro,price=pro.price,quantity=qty)
            messages.success(request,'Was added to cart for new order')


        return redirect('products:product',pro_id=pro_id)
    else: 
        return redirect('products:products')