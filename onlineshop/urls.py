"""onlineshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shop.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home,name='home'),
    path('collections/',collections,name='collections'),
    path('collections/<str:name>',products,name='products'),
    path('collections/<str:cname>/<str:pname>',product_details,name='product_details'),
    path('register/',register,name='register'),
    path('user_login/',user_login,name='user_login'),
    path('user_logout/',user_logout,name='user_logout'),
    path('user_profile/',user_profile,name='user_profile'),
    path('change_password/',change_password,name='change_password'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('cart',cart,name='cart'),
    path('cart_page/',cart_page,name='cart_page'),
    path('remove_cart/<str:cid>',remove_cart,name='remove_cart'),
    path('fav',fav,name='fav'),
    path('fav_page/',fav_page,name='fav_page'),
    path('remove_fav/<str:fid>',remove_fav,name='remove_fav'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

