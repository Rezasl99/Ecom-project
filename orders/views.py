from django.shortcuts import render , redirect
from .forms import OrderForm
from carts.models import CartItem
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def payments(request):
    if request.method == 'POST':  # Ensure it's a POST request
        try:
            # Capture and decode the request body
            body = json.loads(request.body.decode('utf-8'))
            print(body)  # Print the body content

            # Optionally, you can process the body content here, like saving to the database
            
        except json.JSONDecodeError:
            print("Error decoding the request body")
        
    return redirect('home')



def place_order(request, total= 0, quantity= 0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0 :
        return redirect('store')


    final_total = 0
    tax = 0 
    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (10 * total)/100
    final_total = total + tax


    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = final_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            #Order number generator
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user= current_user, is_ordered=False, order_number= order_number)
            order.is_ordered = True
            order.save()

            #Fake payment
            payment = Payment(
                    user= current_user,
                    payment_id = order_number,
                    payment_method= 'paypal',
                    amount_paid= final_total,
                    status= 'success'
                )
            payment.save()
            #order product creation
            cart_items = CartItem.objects.filter(user= current_user)

            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.payment = payment
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.product_price
                orderproduct.ordered = True
                orderproduct.save()


                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variation.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variation)
                orderproduct.save()

                # Reduce the quantity of the sold products
                product = Product.objects.get(id=item.product_id)
                product.product_stock -= item.quantity
                product.save()



            #deleting the cart
            CartItem.objects.filter(user=request.user).delete()


                # Send order recieved email to customer
            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            mail_subject = 'Thank you for your order!'
            message = render_to_string('orders/order_recieved_email.html', {
                'user': current_user,
                'order': order,
                'ordered_products': ordered_products,
            })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            order = Order.objects.get(order_number=order_number, is_ordered=True)

        context = {
                'order_number' : order_number,
                'ordered_products': ordered_products,
                'order':order,
                'cart_items': cart_items,
                'total' : total,
                'tax' : tax,
                'final_total' : final_total,
            }
        print(order_number, current_user)
        return render(request, 'orders/order_complete.html', context)
    else:
        return render(request, 'orders/order_complete.html', context)

