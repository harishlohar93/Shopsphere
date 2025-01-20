from django.shortcuts import get_object_or_404, redirect , render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from .models import Cart, CartItem
from products.models import Product, SizeVariant,ColorVariant

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, uid=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Capture the selected color and size (coming from form submission)
    color_id = request.POST.get('color_variant')  
    size_id = request.POST.get('size_variant')  
    color_variant = ColorVariant.objects.get(id=color_id) if color_id else None
    size_variant = SizeVariant.objects.get(id=size_id) if size_id else None

    # Either create a new cart item or update the existing one
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, color_variant=color_variant, size_variant=size_variant
    )
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart:cart_detail")  # You can redirect to the cart page


#### View Cart
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/cart_detail.html", {"cart": cart})

#### Update Cart Item
@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))
        new_size = request.POST.get("size_variant", item.size_variant)  # Keep existing size if not updated
        new_color = request.POST.get("color_variant", item.color_variant)  # Keep existing color if not updated
        
        # Update cart item
        if new_quantity > 0:
            item.quantity = new_quantity
        elif new_size:
            item.size = new_size
        elif new_color:
            item.color = new_color
        item.save()

    return redirect("cart:cart_detail")

#### Remove Cart Item
@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart:cart_detail")
