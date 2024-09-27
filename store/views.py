from django.shortcuts import render, get_object_or_404 
from .models import Product , Variations
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator
from itertools import chain
from django.db.models import Q

#ویو فروشگاه
def store(request, category_slug=None):
    categories = None 
    if category_slug != None:
        categories = get_object_or_404(Category, category_slug = category_slug)
        products = Product.objects.filter(is_available=True, category=categories)
        product_not_available = Product.objects.all().filter(is_available=False, category=categories)
        
    else:
        products = Product.objects.all().filter(is_available=True)
        product_not_available = Product.objects.all().filter(is_available=False)
    product_count = products.count() + product_not_available.count()
    all_products = list(chain(products , product_not_available))
    paginator = Paginator(all_products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products' : paged_products,
        'product_count' : product_count,
        
    }
    return render(request, 'store/store.html', context)


#ویو برای هر یک از محصولات
def product_detail(request,category_slug, product_slug):
    try:       
        single_product = Product.objects.get(category__category_slug = category_slug, product_slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e 
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
    keyword = request.GET.get('keyword')
    products = Product.objects.none()
    if keyword:
        products = Product.objects.filter(Q(product_name__icontains = keyword) | Q(product_description__icontains = keyword))
    product_count = products.count()
    context = {
        'product_count' : product_count,
        'products': products
    }
    return render (request, 'store/store.html', context)