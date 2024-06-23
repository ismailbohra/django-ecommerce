from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField(max_length=300)
    
    def __str__(self) :
        return self.full_name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        if self.parent:
            return f"{self.name} ({self.parent.name})"
        else:
            return self.name
    def get_category_tree():
        # Fetch categories with no parent
        root_categories = Category.objects.filter(parent=None)

        # Initialize an empty list to store the nested category structure
        category_tree = []

        # Function to build nested category structure recursively
        def build_category_tree(category):
            category_dict = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'children': []
            }
            children = category.children.all()
            for child in children:
                category_dict['children'].append(build_category_tree(child))
            return category_dict

        # Build category tree for each root category
        for root_category in root_categories:
            category_tree.append(build_category_tree(root_category))

        return category_tree

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')

    def __str__(self):
        return f"Image for {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    payment_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    address = models.TextField(default="")
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    card_type = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)  # Format: MM/YY

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"OrderItem #{self.id} - {self.product.name}"