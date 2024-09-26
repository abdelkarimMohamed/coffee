from django.shortcuts import render,get_object_or_404
from .models import Product

# Create your views here.
def products(request):
    products=Product.objects.all()
    return render(request,'products/products.html',{'products':products})

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