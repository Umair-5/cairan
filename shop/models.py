from django.db import models
import uuid
from django.utils.text import slugify
from django.contrib.sessions.models import Session
# Create your models here.

class Product(models.Model):
    unique_id=models.UUIDField(default=uuid.uuid4,editable=True, unique=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
class Cart(models.Model):
    session_key = models.CharField(max_length=40)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)  
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Session {self.session_key}: {self.product.name} ({self.size})"

class Order(models.Model):
    customer_id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(max_length=50)
    customer_address = models.TextField()
    customer_number = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_city=models.CharField(max_length=50)
    customer_state=models.CharField(max_length=50)
    customer_country=models.CharField(max_length=50)
    order_completed = models.BooleanField(default=False, editable=True)
    order_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        formatted_date = self.order_date.strftime('%Y-%m-%d %I:%M %p')
        return f"{self.customer_name} - {formatted_date}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_id = models.UUIDField()
    product_quantity = models.PositiveIntegerField()
    product_size = models.CharField(max_length=10)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} - {self.product_quantity} x {self.product_size}"
