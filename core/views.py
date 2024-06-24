from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from .forms import ContactForm,ProductForm
from django.contrib import messages
from .models import Contact , Product ,Category
from django.views.decorators.csrf import csrf_exempt
from .models import Order,OrderItem
from django.contrib.auth.decorators import login_required




def home(request):
    products = Product.objects.prefetch_related('images').all()
    categories_tree = Category.get_category_tree()
    return render(request,'home.html',{'products':products,'categories_tree':categories_tree})

def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.prefetch_related('images').filter(name__icontains=query) if query else []
    flag=False
    if not products:
        flag=True
        products= Product.objects.prefetch_related('images').all()
    
    related_products=[]
    
    if not flag:
        categories = products.values_list('category', flat=True).distinct()
        related_products = Product.objects.prefetch_related('images').filter(category__in=categories).exclude(id__in=products.values_list('id', flat=True))

    return render(request, 'search.html', {'products': products, 'query': query ,'flag':flag , 'rproducts':related_products})


def about(request):
    return render(request,'about.html')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            msg = Contact.objects.create(
                full_name=full_name,
                email=email,
                message=message
            )
            if msg is not None:
                messages.success(request, 'Successfull.') 
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('addproduct') 
    else:
        form = ProductForm()
    
    return render(request, 'addproduct.html', {'form': form})

def ProductDetails(request, id):
    product = get_object_or_404(Product.objects.prefetch_related('images','category'), id=id)
    rproducts=Product.objects.prefetch_related('images').filter(category=product.category).exclude(id=product.id)
    def build_category_hierarchy(category, category_list):
        category_list.append({'name': category.name, 'id': category.id})
        if category.parent:
            build_category_hierarchy(category.parent, category_list)
        return category_list

    
    category_hierarchy = []
    
    
    category_hierarchy = build_category_hierarchy(product.category, category_hierarchy)
    category_hierarchy.reverse()
    
    return render(request, 'productdetails.html', {'product': product , 'categories' : category_hierarchy , 'rproducts':rproducts})

def get_subcategories(category):
    subcategories = category.children.all()
    all_subcategories = list(subcategories)
    for subcategory in subcategories:
        all_subcategories.extend(get_subcategories(subcategory))
    return all_subcategories

def categorywise(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = get_subcategories(category)
    all_categories = [category] + subcategories
    
    products = Product.objects.filter(category__in=all_categories).prefetch_related('images')
    
    sort_by = request.GET.get('sort', None)
    
    if sort_by == 'latest':
        products = products.order_by('-created_at')  # Assuming 'created_at' is the field for the latest date
    elif sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    
    
    categories_tree = Category.get_category_tree()
    
    return render(request, 'category.html', {'products': products, 'category': category , 'categories_tree' : categories_tree,'current_sort': sort_by })





@login_required
def checkout(request):
    return render(request, 'checkout.html')

@login_required
def payment(request):
    if request.method == 'POST':
        order_total = 0
        req_products = request.POST.get('products_submit', '')
        req_products_list = req_products.split(',')
        
        order_items = []
        for item in req_products_list:
            product_id, product_count = item.split(' ')
            product_count = int(product_count)
            product = get_object_or_404(Product, id=product_id)
            order_total += product.price * product_count
            
            order_items.append({
                'product': product,
                'price': product.price,
                'quantity': product_count
            })
        
        order = Order.objects.create(
            user=request.user,
            status="pending",
            order_total=order_total,
            state=request.POST.get('state', ''),
            city=request.POST.get('city', ''),
            zip_code=request.POST.get('zip_code', ''),
            address=request.POST.get('address', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            card_type=request.POST.get('card_type', ''),
            card_number=request.POST.get('card_number', ''),
            expiration_date=request.POST.get('expiration_date', '')
        )

        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        request.session['order_id'] = order.id
        return redirect('payment-response')
    
    return render(request, 'checkout.html')

@login_required
def placeorder(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = Order.objects.get(id=order_id)
        return render(request, 'placeorder.html', {'order': order})
    else:
        return redirect('/')  

    

@csrf_exempt
def payment_response(request):
        order_id = request.session.get('order_id')
        if order_id:
            order = Order.objects.get(id=order_id) 
            order.payment_status = 'Paid'  
            order.save()
        return redirect('place_order')
    

def myorders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'orders.html',{'orders':orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()  # Related name 'items' is used to fetch order items
    return render(request, 'orderdetails.html', {
        'order': order,
        'order_items': order_items
    })