from django.shortcuts import render,redirect
from django.contrib import messages
# Create your views here.

def signin(request):

    if request.method=='POST' and 'btnlogin' in request.POST:

        messages.info(request,'this is post and btn')
        return redirect('accounts:signin')
    else:
        return render(request,'accounts/signin.html')

def signup(request):

    if request.method=='POST' and 'btnsignup' in request.POST:

        messages.info(request,'this is post and btn')
        return redirect('accounts:signup')
    else:
        return render(request,'accounts/signup.html')

def profile(request):
    
    if request.method=='POST' and 'btnsave' in request.POST:

        messages.info(request,'this is post and btn')
        return redirect('accounts:profile')
    else:
        return render(request,'accounts/profile.html')
