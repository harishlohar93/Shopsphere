from django.shortcuts import render, get_object_or_404
from products.models import Product

def get_product(request, slug):
    # Fetch product or return 404 if not found
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/products.html', {'product': product})
