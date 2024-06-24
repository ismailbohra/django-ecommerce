from django.contrib import admin
from .models import Contact , Product,Category,Image,Order,OrderItem
# Register your models here.

admin.site.register([Contact,Category,Product,Image,Order,OrderItem])