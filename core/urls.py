from django.contrib import admin
from django.urls import path,include

from core import views


urlpatterns = [
    path('',views.home, name='home'),
    path('<int:id>',views.ProductDetails, name='product_details'),
    path('contact',views.contact, name='contact'),
    path('about',views.about, name='about'),
    path('addproduct',views.add_product, name='addproduct'),
    path('checkout',views.checkout, name='checkout'),
    path('myorders',views.myorders, name='myorders'),
    path('myorders/<int:order_id>/',views.order_detail, name='order_detail'),
    path('category/<int:category_id>/', views.categorywise, name='categorywise'),
    path('payment/', views.payment, name='payment'),
    path('payment-response/', views.payment_response, name='payment-response'),
    path('place-order/', views.placeorder, name='place_order'),
    path('search/', views.search_products, name='search_products'),
]
