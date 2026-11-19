from .cart import get_cart


def cart_globals(request):
    """Inject `cart_count` into every template context."""
    cart = get_cart(request, create=False)
    return {
        'cart_count': cart.total_items if cart else 0,
    }
