from .cart import get_cart
from .models import Category


def store_globals(request):
    """Available in every template: `nav_categories` and `cart_count`."""
    cart = get_cart(request, create=False)
    return {
        'nav_categories': Category.objects.all(),
        'cart_count': cart.total_items if cart else 0,
    }
