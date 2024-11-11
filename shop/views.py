from django.shortcuts import render, get_object_or_404
from .models import Product
# Create your views here.

def shop(request):
    products=Product.objects.all()
    return render(request,'shop.html', {'products':products})

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    all_products=Product.objects.exclude(slug=slug)
    return render(request, 'product.html', {'product': product , 'all_products':all_products})

