from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        if not email:
            raise ValueError('Please provide email')
        nemail=self.normalize_email(email)
        user=self.model(email=nemail,name=name)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,name,password):
        user=self.create_user(email,name,password)
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']

    objects=CustomUserManager()


class UserProfile(models.Model):
    profile=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='User images')



class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='Category images')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100)
    p_image=models.ImageField(upload_to='Product images')
    quantity=models.IntegerField()
    original_price=models.FloatField()
    selling_price=models.FloatField()
    specification=models.TextField(max_length=1000)
    trending=models.BooleanField(default=False,help_text='0-Default,1-Trending')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product_qty*self.product.selling_price

class Favorite(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    