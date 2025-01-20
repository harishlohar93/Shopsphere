from django.shortcuts import render
from products.models import Product

# Create your views here.


def home_page(request):
    # for populating the home page with products
    context = {
        'products': Product.objects.all(),

    }
    
    return render(request, 'home/home_page.html', context)
