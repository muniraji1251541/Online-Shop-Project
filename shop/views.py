from django.shortcuts import render,redirect
from shop.models import *
from shop.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import json
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request,'shop/home.html')

def collections(request):
    category=Category.objects.all()
    d={'category':category}
    return render(request,'shop/collections.html',d)

def products(request,name):
    if Category.objects.filter(name=name):
        products=Product.objects.filter(category__name=name)
        d={'products':products,'category_name':name}
        return render(request,'shop/products.html',d)

def product_details(request,cname,pname):
    if Category.objects.filter(name=cname):
        if Product.objects.filter(name=pname):
            products=Product.objects.filter(name=pname)[0]
            d={'products':products}
            return render(request,'shop/product_details.html',d)
        

def register(request):
    cuf=CustomUserForm()
    puf=ProfileUserForm()
    d={'cuf':cuf,'puf':puf}
    if request.method=='POST' and request.FILES:
        cfd=CustomUserForm(request.POST)
        pfd=ProfileUserForm(request.POST,request.FILES)

        if cfd.is_valid() and pfd.is_valid():
            cfo=cfd.save(commit=False)
            password=cfd.cleaned_data['password']
            cfo.set_password(password)
            cfo.save()

            pfo=pfd.save(commit=False)
            pfo.profile=cfo
            pfo.save()

            send_mail('Registration','Thank you for registration','muniraji1251541@gmail.com',[cfo.email],fail_silently=False)

            messages.success(request,'Registration done you can login now!')
    return render(request,'shop/register.html',d)

def user_login(request):
    if request.method=='POST':
        email=request.POST['em']
        password=request.POST['pw']

        user=authenticate(email=email,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['email']=email
            messages.success(request,'LoggedIn successfully')
            return redirect('home')
        else:
            messages.success(request,'First register and then login or invalid password')
    return render(request,'shop/user_login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'LoggedOut Successfully done')
    return redirect('home')

@login_required
def user_profile(request):
    email=request.session.get('email')
    uo=CustomUser.objects.get(email=email)
    po=UserProfile.objects.get(profile=uo)
    d={'uo':uo,'po':po}
    return render(request,'shop/profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        op=request.POST['op']
        np=request.POST['np']
        email=request.session.get('email')
        user=CustomUser.objects.get(email=email)
        check=user.check_password(op)
        if check==True:
            user.set_password(np)
            user.save()
            messages.success(request,'Password changed successfully. You can login now!')
            return redirect('home')
        else:
            messages.success(request,'Incorrect Old Password')
            return redirect('user_profile')
    return render(request,'shop/change_password.html')

def forgot_password(request):
    if request.method=='POST':
        em=request.POST['email']
        password=request.POST['pass']
        user=CustomUser.objects.filter(email=em)
        if user:
            userobj=user[0]
            userobj.set_password(password)
            userobj.save()
            messages.success(request,'Password Reset successfully. You can login now!')
            return redirect('user_login')
        else:
            messages.success(request,'Your email did not match')
            
    return render(request,'shop/forgot_password.html')

def cart(request):
    if request.headers.get('X-Requested-Width')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'Product already added'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock not available'},status=200)

        else:
            return JsonResponse({'status':'First Login and then add'},status=200)
        
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)


def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        d={'cart':cart}
        return render(request,'shop/cart_page.html',d)
    else:
        return render(request,'shop/cart_page.html')

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('cart_page')

def fav(request):
    if request.headers.get('X-Requested-Width')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_id=data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favorite.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'Product already added'},status=200)
                else:
                    Favorite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product added to Favorite'},status=200)

        else:
            return JsonResponse({'status':'First Login and then add'},status=200)
        
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def fav_page(request):
    if request.user.is_authenticated:
        fav=Favorite.objects.filter(user=request.user)
        d={'fav':fav}
        return render(request,'shop/fav_page.html',d)
    else:
        return render(request,'shop/fav_page.html')

def remove_fav(request,fid):
    favitem=Favorite.objects.get(id=fid)
    favitem.delete()
    return redirect('fav_page')