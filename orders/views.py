import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from cart.context_processors import get_or_create_cart
from restaurants.models import Restaurant
from .models import Order, OrderItem, Coupon


@login_required
def check_new_orders(request):
    restaurant = Restaurant.objects.filter(owner=request.user).first()
    if not restaurant and request.user.is_superuser:
        restaurant = Restaurant.objects.first()

    if not restaurant:
        return JsonResponse({'new_orders': 0})

    # Check for orders placed in the last 25 seconds
    recent_orders = Order.objects.filter(
        restaurant=restaurant,
        created_at__gte=timezone.now() - timezone.timedelta(seconds=25)
    )
    
    recent_count = recent_orders.count()
    latest_order = recent_orders.order_by('-created_at').first()
    order_num = latest_order.order_number if latest_order else ""

    return JsonResponse({
        'new_orders': recent_count,
        'latest_order_number': order_num,
    })


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty. Add items before checkout!")
        return redirect('restaurant_list')

    restaurant = cart.get_restaurant
    subtotal = float(cart.get_subtotal)
    delivery_fee = 40 if subtotal > 0 else 0
    tax = round(subtotal * 0.05, 2)

    coupon_code = request.session.get('coupon_code', '')
    discount = 0.0

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code__iexact=coupon_code, active=True)
            discount = float(coupon.calculate_discount(subtotal))
        except Coupon.DoesNotExist:
            request.session.pop('coupon_code', None)
            request.session.pop('coupon_discount', None)

    total = max(0.0, subtotal + float(delivery_fee) + tax - discount)

    if request.method == "POST":
        address = request.POST.get('delivery_address', '').strip()
        phone = request.POST.get('phone', '').strip()
        payment_method = request.POST.get('payment_method', 'COD')
        special_notes = request.POST.get('special_notes', '')

        if not address or not phone:
            messages.error(request, "Please fill in your delivery address and phone number.")
            return redirect('checkout')

        payment_status = 'Paid' if payment_method in ['UPI', 'Card', 'NetBanking', 'PayPal'] else 'Pending'

        order = Order.objects.create(
            customer=request.user,
            restaurant=restaurant,
            delivery_address=address,
            phone=phone,
            special_notes=special_notes,
            payment_method=payment_method,
            payment_status=payment_status,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            tax_amount=tax,
            discount_amount=discount,
            total_amount=round(total, 2),
            coupon_code=coupon_code,
            status='Confirmed'
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                food_name=item.menu_item.food_name,
                price=item.menu_item.price,
                quantity=item.quantity,
                special_instructions=item.special_instructions
            )

        # Clear cart and session coupon
        cart.items.all().delete()
        request.session.pop('coupon_code', None)
        request.session.pop('coupon_discount', None)

        messages.success(request, f"Order #{order.order_number} placed successfully!")
        return redirect('order_confirmation', order_number=order.order_number)

    context = {
        'cart': cart,
        'restaurant': restaurant,
        'subtotal': round(subtotal, 2),
        'delivery_fee': delivery_fee,
        'tax': tax,
        'discount': round(discount, 2),
        'total': round(total, 2),
        'coupon_code': coupon_code,
        'user': request.user,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def paypal_complete_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            address = data.get('delivery_address', 'Default Address')
            phone = data.get('phone', request.user.phone or '9999999999')
            transaction_id = data.get('transaction_id', '')

            cart = get_or_create_cart(request)
            if not cart.items.exists():
                return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)

            restaurant = cart.get_restaurant
            subtotal = float(cart.get_subtotal)
            delivery_fee = 40 if subtotal > 0 else 0
            tax = round(subtotal * 0.05, 2)
            coupon_code = request.session.get('coupon_code', '')
            discount = float(request.session.get('coupon_discount', 0))

            total = max(0.0, subtotal + float(delivery_fee) + tax - discount)

            order = Order.objects.create(
                customer=request.user,
                restaurant=restaurant,
                delivery_address=address,
                phone=phone,
                payment_method='PayPal',
                payment_status='Paid',
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                tax_amount=tax,
                discount_amount=discount,
                total_amount=round(total, 2),
                coupon_code=coupon_code,
                special_notes=f"PayPal Transaction ID: {transaction_id}",
                status='Confirmed'
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    menu_item=item.menu_item,
                    food_name=item.menu_item.food_name,
                    price=item.menu_item.price,
                    quantity=item.quantity,
                    special_instructions=item.special_instructions
                )

            # Clear cart
            cart.items.all().delete()
            request.session.pop('coupon_code', None)
            request.session.pop('coupon_discount', None)

            messages.success(request, f"PayPal Payment Successful! Order #{order.order_number} confirmed.")
            return JsonResponse({'status': 'success', 'order_number': order.order_number})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def apply_coupon(request):
    code = (request.POST.get('coupon_code') or request.GET.get('coupon_code') or '').strip()
    cart = get_or_create_cart(request)
    subtotal = float(cart.get_subtotal)

    if code:
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            if subtotal < float(coupon.min_order_amount):
                messages.error(request, f"Minimum order amount for coupon '{code}' is ₹{coupon.min_order_amount}")
            else:
                discount = float(coupon.calculate_discount(subtotal))
                request.session['coupon_code'] = coupon.code
                request.session['coupon_discount'] = discount
                messages.success(request, f"🎉 Coupon '{coupon.code}' applied! You saved ₹{discount:.2f}.")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")

    next_url = request.META.get('HTTP_REFERER') or 'cart_detail'
    return redirect(next_url)


def remove_coupon(request):
    request.session.pop('coupon_code', None)
    request.session.pop('coupon_discount', None)
    messages.info(request, "Coupon removed.")
    next_url = request.META.get('HTTP_REFERER') or 'cart_detail'
    return redirect(next_url)


@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, customer=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})


@login_required
def order_tracking(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    
    status_steps = [
        ('Pending', 15),
        ('Confirmed', 30),
        ('Preparing', 55),
        ('Ready for Pickup', 75),
        ('Out for Delivery', 90),
        ('Delivered', 100),
    ]
    
    current_progress = 0
    for status_name, pct in status_steps:
        if order.status == status_name:
            current_progress = pct
            break
    if order.status == 'Cancelled':
        current_progress = 0

    return render(request, 'orders/order_tracking.html', {
        'order': order,
        'progress_pct': current_progress,
    })


@login_required
def customer_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/customer_orders.html', {'orders': orders})


@login_required
def order_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_invoice.html', {'order': order})


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            if new_status == 'Delivered':
                order.payment_status = 'Paid'
            order.save()
            messages.success(request, f"Order #{order.order_number} status updated to {new_status}")
    next_url = request.META.get('HTTP_REFERER') or 'restaurant_dashboard'
    return redirect(next_url)


@login_required
def delivery_dashboard(request):
    available_orders = Order.objects.filter(
        status__in=['Confirmed', 'Preparing', 'Ready for Pickup'],
        delivery_partner__isnull=True
    ).order_by('-created_at')

    my_deliveries = Order.objects.filter(
        delivery_partner=request.user
    ).order_by('-updated_at')

    if request.method == "POST":
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        if action == 'claim':
            order.delivery_partner = request.user
            order.save()
            messages.success(request, f"You accepted delivery for Order #{order.order_number}")
        elif action == 'update_status':
            new_status = request.POST.get('status')
            if new_status in ['Out for Delivery', 'Delivered']:
                order.status = new_status
                if new_status == 'Delivered':
                    order.payment_status = 'Paid'
                order.save()
                messages.success(request, f"Updated status of #{order.order_number} to {new_status}")
        return redirect('delivery_dashboard')

    context = {
        'available_orders': available_orders,
        'my_deliveries': my_deliveries,
    }
    return render(request, 'orders/delivery_dashboard.html', context)
