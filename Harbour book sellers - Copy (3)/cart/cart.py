from .models import Cart


def get_cart(request, create=True):
    """Return the Cart for the current session, optionally creating one."""
    if not request.session.session_key:
        if not create:
            return None
        request.session.create()
    key = request.session.session_key
    if create:
        cart, _ = Cart.objects.get_or_create(session_key=key)
        return cart
    return Cart.objects.filter(session_key=key).first()
