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
            
            if OrderDetails.objects.all().filter(order=old_order,product=pro).exists():
                orderDetail=OrderDetails.objects.get(order=old_order,product=pro)
                orderDetail.quantity+=int(qty)
                orderDetail.save()
            else:
                orderDetails=OrderDetails.objects.create(order=old_order,product=pro,price=pro.price,quantity=qty)
            messages.success(request,'Was added to cart for old order')


        else:
            new_order=Order.objects.create(user=request.user,order_date=timezone.now(),is_finished=False)
            OrderDetails.objects.create(order=new_order,product=pro,price=pro.price,quantity=qty)
            messages.success(request,'Was added to cart for new order')


        return redirect('products:product',pro_id=pro_id)
    else:
        if 'pro_id' in request.GET:

            messages.error(request,'You musr be logged in')
            pro_id = request.GET.get('pro_id')
            return redirect('products:product',pro_id=pro_id)
        else: 
            return redirect('index')
    
def cart(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False).exists():

            order=Order.objects.get(user=request.user,is_finished=False)

            orderdetails=OrderDetails.objects.all().filter(order=order)
            total=0
            for orderdetail in orderdetails:
                total+=orderdetail.price * orderdetail.quantity
            context={
                'orderdetails':orderdetails,
                'order':order,
                'total':total,
            }
    return render(request,'orders/cart.html',context)

def remove_from_cart(request,orderdetails_id):
    
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:

        orderdetails=OrderDetails.objects.get(id=orderdetails_id)

        if request.user.id == orderdetails.order.user.id:
             
            orderdetails.delete()

    return redirect('add_to_cart:cart')

def add_qty(request,orderdetails_id):

    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:

        orderdetails=OrderDetails.objects.get(id=orderdetails_id)
        if request.user.id == orderdetails.order.user.id:

            orderdetails.quantity +=1
            orderdetails.save()

    return redirect('add_to_cart:cart')
 
def sub_qty(request,orderdetails_id):

    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:

        orderdetails=OrderDetails.objects.get(id=orderdetails_id)
        
        if request.user.id == orderdetails.order.user.id:

            if orderdetails.quantity > 1:

                orderdetails.quantity -=1
                orderdetails.save()
            
    return redirect('add_to_cart:cart')