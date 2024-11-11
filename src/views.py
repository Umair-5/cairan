from django.shortcuts import render,redirect
from shop.models import *
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        session_key = request.session.session_key

        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        product = Product.objects.get(unique_id=product_id)
        cart_item = Cart.objects.filter(session_key=session_key, product=product, size=size).first()

        if cart_item:
            return JsonResponse({'success': True, 'message': 'Product is already in cart'})
        else:
            cart_item = Cart(session_key=session_key, product=product, size=size, quantity=1)
            cart_item.save()
            return JsonResponse({'success': True, 'message': 'Product added to cart'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_cart_items(request):
    session_key = request.session.session_key
    cart_items = Cart.objects.filter(session_key=session_key)

    items_data = [{
        'product_id': item.product.unique_id,
        'size': item.size,
        'quantity': item.quantity,
        'price': item.product.price,
    } for item in cart_items]

    return JsonResponse({'cart_items': items_data})

def cart(request):
    session_key = request.session.session_key
    cart_items = Cart.objects.filter(session_key=session_key)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def delete_item(request, item_id):
    if request.method == 'DELETE':
        session_key = request.session.session_key
        Cart.objects.filter(session_key=session_key, product__unique_id=item_id).delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def update_quantity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            size = data.get('size')
            action = data.get('action')
            session_key = request.session.session_key
            
            if product_id and size and action:
                cart_item = Cart.objects.filter(session_key=session_key, product__unique_id=product_id, size=size).first()

                if action == 'increase':
                    cart_item.quantity += 1
                    cart_item.save()
                elif action == 'decrease':
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                    else:
                        return JsonResponse({'status': 'failed', 'message': 'Quantity cannot be less than 1'})
                cart_items = Cart.objects.filter(session_key=session_key)
                total_price = sum(item.product.price * item.quantity for item in cart_items)
                return JsonResponse({'status': 'success', 'quantity': cart_item.quantity, 'total_price': total_price})

            else:
                return JsonResponse({'error': 'Missing data'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



def checkout(request):
    session_key = request.session.session_key
    cart_items = Cart.objects.filter(session_key=session_key)

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def place_order(request):
    if request.method=='POST':
        data= json.loads(request.body)
        customer_name = data.get('customer_name')
        customer_number = data.get('customer_number')
        customer_email = data.get('customer_email')
        customer_address = data.get('customer_address')
        customer_city= data.get('customer_city')
        customer_state= data.get('customer_state')
        customer_country= data.get('customer_country')
        session_key = request.session.session_key
        cart_items = Cart.objects.filter(session_key=session_key)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            customer_name=customer_name,
            customer_number=customer_number,
            customer_email=customer_email,
            customer_address=customer_address,
            customer_city=customer_city,
            customer_state=customer_state,
            customer_country=customer_country,
            order_completed=False,
            total_price=total_price
        )
        order.save()
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                product_id=item.product.unique_id,
                product_quantity=item.quantity,
                product_size=item.size,
                item_price=item.product.price
            ).save()
        cart_items.delete()    
        return JsonResponse({'success': True})   
             
    else:
        return JsonResponse({'error': 'Order not placed'}, status=405)
