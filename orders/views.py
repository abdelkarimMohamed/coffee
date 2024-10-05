from django.shortcuts import render,redirect
from django.contrib import messages
from products.models import Product
from .models import Order,OrderDetails,Payment
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

def payment(request):
    context=None
    ship_address=None
    ship_phone=None
    card_number=None
    expire=None
    security_code=None
    is_added=None
    

    if request.method == 'POST' and 'btnpayment' in request.POST and 'ship_address' in request.POST and 'ship_phone' in request.POST and 'card_number' in request.POST and 'expire' in request.POST and 'security_code' in request.POST:

        ship_address=request.POST['ship_address']
        ship_phone=request.POST['ship_phone']
        card_number=request.POST['card_number']
        expire=request.POST['expire']
        security_code=request.POST['security_code']

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False).exists():

                order=Order.objects.get(user=request.user,is_finished=False)
                payment=Payment(order=order,shipment_address=ship_address,shipment_phone=ship_phone,card_number=card_number,expire=expire,security=security_code)
                payment.save()
                order.is_finished=True
                order.save()
                is_added=True
                messages.success(request,'Your order is finished')
        context={
            'ship_address':ship_address,
            'ship_phone':ship_phone,
            'card_number':card_number,
            'expire':expire,
            'security_code':security_code,
            'is_added':is_added,
        }
    else:
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
    return render(request,'orders/payment.html',context)

def show_orders(request):

    context=None
    all_orders=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders=Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
                order=Order.objects.get(id=x.id)
                orderdetails=OrderDetails.objects.all().filter(order=order)
                total=0
                for orderdetail in orderdetails:
                    total+=orderdetail.price * orderdetail.quantity
                x.total=total
                x.items_count=orderdetails.count
    context={
        'all_orders':all_orders
    }

    return render(request,'orders/show_orders.html',context)
