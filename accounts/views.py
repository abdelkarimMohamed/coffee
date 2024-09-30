from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from products.models import Product
import re
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# from django.contrib.auth.hashers import check_password



# Create your views here.

def signin(request):

    if request.method=='POST' and 'btnlogin' in request.POST:
        print(request.POST)
        username=request.POST['user']
        password=request.POST['pass']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            login(request,user)
        else:
            messages.error(request,'Username or Password invalid')

        return redirect('accounts:signin')
    else:
        return render(request,'accounts/signin.html')
@login_required    
def user_logout(request):

    logout(request)
    return redirect('index')

def signup(request):

    if request.method=='POST' and 'btnsignup' in request.POST:

        fname=None
        lname=None
        address=None
        address2=None
        city=None
        state=None
        zip_number=None
        email=None
        username=None
        password=None
        terms=None
        is_added=None

        if 'fname' in request.POST: fname=request.POST['fname']
        else: messages.error(request,'Error in First Name')
        if 'lname' in request.POST: lname=request.POST['lname']
        else: messages.error(request,'Error in Last Name')
        if 'address' in request.POST: address=request.POST['address']
        else: messages.error(request,'Error in Adrress')
        if 'address2' in request.POST: address2=request.POST['address2']
        else: messages.error(request,'Error in Adrress2')
        if 'city' in request.POST: city=request.POST['city']
        else: messages.error(request,'Error in city')
        if 'state' in request.POST: state=request.POST['state']
        else: messages.error(request,'Error in state')
        if 'zip' in request.POST: zip_number=request.POST['zip']
        else: messages.error(request,'Error in zip')
        if 'email' in request.POST: email=request.POST['email']
        else: messages.error(request,'Error in email')
        if 'user' in request.POST: username=request.POST['user']
        else: messages.error(request,'Error in username')
        if 'pass' in request.POST: password=request.POST['pass']
        else: messages.error(request,'Error in password')
        if 'terms' in request.POST: terms=request.POST['terms']

        if fname and lname and address and address2 and city and state and zip_number and email and username and password:
            if terms == 'on':
                if User.objects.filter(username=username).exists():

                    messages.error(request,'This Username is Taken')
                else:
                    if User.objects.filter(email=email).exists():
                         messages.error(request,'This Email is Taken')
                    else:
                        patt="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                        if re.match(patt,email):
                            user=User.objects.create(first_name=fname,last_name=lname,email=email,username=username)
                            user.set_password(password)
                            user.save()
                            userprofile=UserProfile.objects.create(user=user,address=address,address2=address2,city=city,state=state,zip_number=zip_number)
                            userprofile.save()
                            fname=''
                            lname=''
                            address=''
                            address2=''
                            city=''
                            state=''
                            email=''
                            zip_number=''
                            username=''
                            password=''
                            terms=None
                            messages.success(request,'Your account is created')
                            is_added=True
                        else:
                            messages.error(request,'Invalid email')
            else:
                messages.error(request,'You must agree to the terms')
        else:
            messages.error(request,'Check Empty Fields')
        # messages.info(request,'this is post and btn')
        return render(request,'accounts/signup.html',{
            'fname':fname,
            'lname':lname,
            'address':address,
            'address2':address2,
            'city':city,
            'state':state,
            'email':email,
            'user':username,
            'pass':password,
            'zip':zip_number,
            'is_added':is_added
        })

    else:
        return render(request,'accounts/signup.html')
    
def profile(request):
    
    if request.method=='POST' and 'btnsave' in request.POST:

        if request.user is not None and request.user.id != None:

            userprofile=UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['email'] and request.POST['city'] and request.POST['state'] and request.POST['zip'] and request.POST['user'] and request.POST['pass']:
                request.user.first_name=request.POST['fname']
                request.user.last_name=request.POST['lname']
                userprofile.address=request.POST['address']
                userprofile.address2=request.POST['address2']
                userprofile.city=request.POST['city']
                userprofile.state=request.POST['state']
                userprofile.zip_number=request.POST['zip']
                # if not request.user.check_password(request.POST['pass']):
                # if not check_password(request.POST['pass'], request.user.password):


                if not request.POST['pass'].startswith('pbkdf2_sha256$'):

                    request.user.set_password(request.POST['pass'])
              


                request.user.save()
                userprofile.save()
                login(request,request.user)
                messages.success(request,'Your data has been saved')

            else:
                messages.error(request,'Check your values and elements')

        return redirect('accounts:profile')
    else:
        if request.user is not None:
            context=None
            if not request.user.is_anonymous:
                userprofile=UserProfile.objects.get(user=request.user)
                context={
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'state':userprofile.state,
                    'zip':userprofile.zip_number,
                    'email':request.user.email,
                    'user':request.user.username,
                    'pass':request.user.password,
                }
         
            return render(request,'accounts/profile.html',context)
        else:
            return redirect('accounts:profile')

def product_favorite(request,pro_id):
    
    
    if(request.user.is_authenticated and not request.user.is_anonymous):
        pro_fav=Product.objects.get(pk=pro_id)
        print(pro_fav)
        if UserProfile.objects.filter(user=request.user,product_favorites=pro_fav).exists():
            messages.success(request,'Already product in the favorite list')
        else:
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request,'Product has been favorited')

    else:
        messages.error(request,'You must be logged in')
        
    # return redirect('products:product' + str(pro_id))
    # return reverse("products:product",args=[pro_id])
    return redirect(reverse('products:product', kwargs={'pro_id': pro_id}))

