import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from menu.models import MenuItem
from .models import Cart, CartItem
from .context_processors import get_or_create_cart


def get_ai_recommendations(cart):
    if not cart or not cart.items.exists():
        return []

    cart_restaurant = cart.get_restaurant
    if not cart_restaurant:
        return []

    cart_item_ids = cart.items.values_list('menu_item_id', flat=True)

    available_items = MenuItem.objects.filter(
        restaurant=cart_restaurant,
        is_available=True
    ).exclude(id__in=cart_item_ids)

    ai_suggestions = available_items.filter(is_popular=True)[:4]
    if not ai_suggestions.exists():
        ai_suggestions = available_items[:4]

    return ai_suggestions


def voice_order_process(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            transcript = data.get("transcript", "").strip()

            if not transcript:
                return JsonResponse({"status": "error", "message": "No speech recognized."}, status=400)

            # Search menu items matching transcript
            matched_items = MenuItem.objects.filter(is_available=True)
            direct_match = matched_items.filter(food_name__icontains=transcript).first()

            if not direct_match:
                words = transcript.split()
                for word in words:
                    if len(word) > 2 and word.lower() not in ["order", "one", "two", "please", "food", "a", "and", "the"]:
                        found = matched_items.filter(food_name__icontains=word).first()
                        if found:
                            direct_match = found
                            break

            if direct_match:
                cart = get_or_create_cart(request)
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    menu_item=direct_match,
                    defaults={'quantity': 1}
                )
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()

                messages.success(request, f"🎙️ Voice Recognized: Added '{direct_match.food_name}' to your cart!")
                return JsonResponse({
                    "status": "success",
                    "matched": direct_match.food_name,
                    "redirect": "/cart/"
                })
            else:
                return JsonResponse({
                    "status": "search",
                    "query": transcript,
                    "redirect": f"/menu/?search={transcript}"
                })

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


def cart_detail(request):
    cart = get_or_create_cart(request)
    subtotal = float(cart.get_subtotal)
    delivery_fee = 40 if subtotal > 0 else 0
    tax = round(subtotal * 0.05, 2)
    
    # Coupon from session if set
    discount = float(request.session.get('coupon_discount', 0))
    total = max(0.0, subtotal + float(delivery_fee) + tax - discount)

    ai_recommendations = get_ai_recommendations(cart)

    context = {
        'cart': cart,
        'cart_restaurant': cart.get_restaurant,
        'subtotal': round(subtotal, 2),
        'delivery_fee': delivery_fee,
        'tax': tax,
        'discount': round(discount, 2),
        'total': round(total, 2),
        'coupon_code': request.session.get('coupon_code', ''),
        'ai_recommendations': ai_recommendations,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, menu_id):
    menu_item = get_object_or_404(MenuItem, id=menu_id)
    cart = get_or_create_cart(request)

    # Check if cart has items from another restaurant
    cart_restaurant = cart.get_restaurant
    if cart_restaurant and cart_restaurant != menu_item.restaurant:
        if request.POST.get('clear_and_add'):
            cart.items.all().delete()
        else:
            messages.warning(
                request,
                f"Your cart contains items from '{cart_restaurant.restaurant_name}'. Would you like to clear cart and add items from '{menu_item.restaurant.restaurant_name}'?"
            )
            return redirect('cart_detail')

    quantity = int(request.POST.get('quantity', 1))
    instructions = request.POST.get('instructions', '')

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item,
        defaults={'quantity': quantity, 'special_instructions': instructions}
    )

    if not created:
        cart_item.quantity += quantity
        if instructions:
            cart_item.special_instructions = instructions
        cart_item.save()

    messages.success(request, f"Added {menu_item.food_name} to cart!")
    
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart_detail'
    return redirect(next_url)


def update_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.info(request, "Item removed from cart.")

    return redirect('cart_detail')


def remove_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('cart_detail')


def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    if 'coupon_discount' in request.session:
        del request.session['coupon_discount']
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    messages.info(request, "Cart cleared.")
    return redirect('cart_detail')
