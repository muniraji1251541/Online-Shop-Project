from django.contrib import admin
from shop.models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserProfile)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Favorite)