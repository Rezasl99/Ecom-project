from .models import CartItem
from .views import _cart_id
from django.db.models import Sum

def counter(request):
   
    if 'admin' in request.path:
        return {}

    cart_count = 0
    try:
        cart_id = _cart_id(request)  
        cart_count = CartItem.objects.filter(cart__cart_id=cart_id, is_active=True).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    except CartItem.DoesNotExist:
        cart_count = 0

    return dict(cart_count=cart_count)
