from django.shortcuts import render,get_object_or_404
from .models import Product

# Create your views here.
def products(request):

    products=Product.objects.all()
    cs=request.GET.get('cs')
    if not cs:
        cs='off' 
    name=request.GET.get('searchname')
    if name:
        if cs == 'on':
            products=products.filter(name__contains=name)
        else:
            products=products.filter(name__icontains=name)

    description=request.GET.get('searchdesc')
    if description:
        if cs == 'on':
             products= products.filter(description__contains=description)
        else:
            products= products.filter(description__icontains=description)

    searchpricefrom=request.GET.get('searchpricefrom')
    searchpriceto=request.GET.get('searchpriceto')

    if searchpricefrom and searchpriceto:
        if searchpricefrom.isdigit() and searchpriceto.isdigit():
             products = products.filter(price__gte=searchpricefrom, price__lte=searchpriceto)
    # name=request.GET.get('searchpricefrom')
    # name=request.GET.get('searchpriceto')
    # name=request.GET.get('cs')
    # products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'products/products.html',context)

def product(request,pro_id):

    # product=get_object_or_404(Product,
    #                        name=name,
    #                        publish_data__year=year,
    #                        publish_data__month=month,
    #                        publish_data__day=day,)
    pro=get_object_or_404(Product,pk=pro_id)
    return render(request,'products/product.html',{'pro':pro})

def search(request):
    return render(request,'products/search.html')