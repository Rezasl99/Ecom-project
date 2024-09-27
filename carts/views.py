from django.shortcuts import render, redirect , get_object_or_404
from store.models import Product , Variations
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

#getting unique session key
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


#adding items in the cart
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []  #list to store product variations Example:color and size
    #gets all the variations from each product and adds to to product_variation
    if request.method == 'POST':
        for i in request.POST:
            key = i
            value = request.POST[key]
            try:
                variation = Variations.objects.get(product=product, variation_category__iexact= key, variation_value__iexact = value)
                product_variation.append(variation)
            except:
                pass

#creating or getting the user's cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
#checking whether the same variation of items exist in cart
    cart_item_exists = CartItem.objects.filter(product = product, cart = cart ).exists() #checks whether items exists or not 
    if cart_item_exists:
        cart_item = CartItem.objects.filter(product = product, cart =cart)
        existing_variations_list = []
        id = [] 

        for item in cart_item:
            existing_variations = item.variation.all()
            existing_variations_list.append(list(existing_variations))
            id.append(item.id)

        if product_variation in existing_variations_list:  
            index = existing_variations_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity +=1
            item.save()
        else:
            item = CartItem.objects.create(product=product,quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()
    else: 
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )

        if len(product_variation) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save()
    return redirect('cart')


#deleting items quantity one by one from cart
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    try: 
        cart_item = CartItem.objects.get(cart=cart , product=product , id = cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart')



#deleting the item from cart

def remove_cart_item(request,product_id, cart_item_id):
    cart = Cart.objects.get(cart_id =_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product, id = cart_item_id)
    cart_item.delete()
    return redirect('cart')
    

#cart 
def cart(request,total=0, quantity=0, cart_items=None):
    tax = 0
    final_total = 0
    try:
        cart = Cart.objects.get(cart_id =_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (10 * total)/100
        final_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax ,
        'final_total' : final_total,
    }
    return render (request, 'store/cart.html', context)