from django.shortcuts import render, get_object_or_404 ,redirect
from .models import Product, Variations, ReviewRating , ProductView
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator
from itertools import chain
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
""" View for the store """


def get_client_ip(request):
    """ gets the client Ip before vpn """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def store(request, category_slug=None):
    """ View for the store page """
    categories = None
    if category_slug != None:
        categories = get_object_or_404(Category, category_slug = category_slug)
        products = Product.objects.filter(is_available=True, category=categories)
        product_not_available = Product.objects.all().filter(is_available=False, category=categories)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('-views')
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



def product_detail(request,category_slug, product_slug):
    """ View for the detail of each product """
    try:
        single_product = Product.objects.get(category__category_slug = category_slug, product_slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    #checks whether use bought the product or not
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    else:
        orderproduct = None

    """ View count funtionality """
    # Track views by IP within 24 hours
    ip_address = get_client_ip(request)
    view_time_threshold = timezone.now() - timedelta(hours=24)

    print(f"View Time Threshold: {view_time_threshold}")

    # Check if the same IP has viewed the product in the last 24 hours
    recent_view = ProductView.objects.filter(
        product=single_product,
        ip_address=ip_address,
        timestamp__gte=view_time_threshold
    ).exists()

    print(f"Recent View Exists: {recent_view}")

    if not recent_view:
        # Increment the view count if no recent views
        ProductView.objects.create(product=single_product, ip_address=ip_address)
        single_product.views = F('views') + 1
        single_product.save()
        single_product.refresh_from_db()

    reviews = ReviewRating.objects.filter(product_id = single_product.id, status=True)

    context = {
        'orderproduct' : orderproduct,
        'single_product' : single_product,
        'in_cart' : in_cart,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
    """ Search funtionality view """
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


def submit_review(request, product_id):
    if request.method == 'POST':
        current_url = request.META.get('HTTP_REFERER')
        try:

            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id)
            form = ReviewForm(request.POST, instance= reviews)
            form.save()
            messages.success(request, 'Your review has been updated')
            return redirect(current_url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Your review has been added.')
                return redirect(current_url)
