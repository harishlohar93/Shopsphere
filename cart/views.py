from django.shortcuts import get_object_or_404, redirect , render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from .models import Cart, CartItem
from products.models import Product, SizeVariant,ColorVariant
# import messsages
from django.contrib import messages



@login_required
def add_to_cart(request, product_id):
    # Get the product by its unique ID
    product = get_object_or_404(Product, uid=product_id)

    # Ensure a cart is associated with the logged-in user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Capture the selected color and size from the request (e.g., via a form submission)
    color_id = request.POST.get('color_variant')
    size_id = request.POST.get('size_variant')

    try:
        color_variant = ColorVariant.objects.get(id=color_id) if color_id else None
    except ColorVariant.DoesNotExist:
        messages.error(request, "Selected color variant does not exist.")
        return redirect('cart_detail')

    try:
        size_variant = SizeVariant.objects.get(id=size_id) if size_id else None
    except SizeVariant.DoesNotExist:
        messages.error(request, "Selected size variant does not exist.")
        return redirect('cart_detail')

    # Find or create a cart item based on product and variants
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, color_variant=color_variant, size_variant=size_variant
    )

    # Increment the quantity if the item already exists in the cart
    if not created:
        cart_item.quantity += 1
    
    # Save the cart item
    cart_item.save()
    
    # Notify the user of success
    messages.success(request, f"{product.product_name} has been added to your cart!")

    # Redirect to the cart detail page (replace 'cart_detail' with your actual view name)
    return redirect('cart:cart_detail')

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

# checkout  view
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart/checkout_cart.html", {"cart": cart})
