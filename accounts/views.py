from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
import re
# Create your views here.

def signin(request):

    if request.method=='POST' and 'btnlogin' in request.POST:

        messages.info(request,'this is post and btn')
        return redirect('accounts:signin')
    else:
        return render(request,'accounts/signin.html')

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
                            user=User.objects.create(first_name=fname,last_name=lname,email=email,username=username,password=password)
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

        messages.info(request,'this is post and btn')
        return redirect('accounts:profile')
    else:
        return render(request,'accounts/profile.html')
