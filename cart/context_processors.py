from .models import Cart


def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    if request.user.is_authenticated:
        user_carts = Cart.objects.filter(user=request.user).order_by('-updated_at')
        if user_carts.exists():
            cart = user_carts.first()
            # Clean up any duplicate carts gracefully
            if user_carts.count() > 1:
                for duplicate in user_carts[1:]:
                    for item in duplicate.items.all():
                        existing_item = cart.items.filter(menu_item=item.menu_item).first()
                        if existing_item:
                            existing_item.quantity += item.quantity
                            existing_item.save()
                        else:
                            item.cart = cart
                            item.save()
                    duplicate.delete()
        else:
            # Transfer anonymous session cart to authenticated user if present
            session_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
            if session_cart:
                session_cart.user = request.user
                session_cart.save()
                cart = session_cart
            else:
                cart = Cart.objects.create(user=request.user)
    else:
        session_cart = Cart.objects.filter(session_key=session_key).first()
        if not session_cart:
            session_cart = Cart.objects.create(session_key=session_key)
        cart = session_cart

    return cart


def cart_context(request):
    try:
        cart = get_or_create_cart(request)
        return {
            'cart': cart,
            'cart_count': cart.get_total_quantity,
            'cart_subtotal': cart.get_subtotal,
            'cart_restaurant': cart.get_restaurant,
        }
    except Exception:
        return {
            'cart': None,
            'cart_count': 0,
            'cart_subtotal': 0,
            'cart_restaurant': None,
        }
