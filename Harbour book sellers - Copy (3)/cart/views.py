
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from catalog.models import Book
from .cart import get_cart
from .forms import CheckoutForm
from .models import CartItem, Order, OrderItem


def _is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def _cart_payload(cart):
    return {'cart_count': cart.total_items, 'cart_total': str(cart.total)}


# ── Cart display ──────────────────────────────────────────────────────────────

def cart_view(request):
    cart = get_cart(request)
    items = cart.items.select_related('book')
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total': cart.total,
    })


# ── Cart add ──────────────────────────────────────────────────────────────────

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        qty = max(int(request.POST.get('quantity', 1)), 1)
    except (TypeError, ValueError):
        qty = 1

    cart = get_cart(request)
    item, _ = CartItem.objects.get_or_create(cart=cart, book=book, defaults={'quantity': 0})
    new_qty = min(item.quantity + qty, book.stock or 99)

    if new_qty <= 0:
        item.delete()
        msg, ok = f'"{book.title}" is out of stock.', False
    else:
        item.quantity = new_qty
        item.save(update_fields=['quantity'])
        msg, ok = f'"{book.title}" added to your cart.', True

    if _is_ajax(request):
        return JsonResponse(
            {'ok': ok, 'message': msg, **_cart_payload(cart)},
            status=200 if ok else 409,
        )
    (messages.success if ok else messages.error)(request, msg)
    return redirect(request.META.get('HTTP_REFERER') or 'cart')


# ── Cart update ───────────────────────────────────────────────────────────────

def update_cart(request, book_id):
    cart = get_cart(request)
    try:
        qty = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        qty = 1

    item = CartItem.objects.filter(cart=cart, book_id=book_id).first()
    if not item:
        item = CartItem.objects.filter(cart=cart, id=book_id).first()
    if item:
        if qty <= 0:
            item.delete()
        else:
            item.quantity = min(qty, item.book.stock or 99)
            item.save(update_fields=['quantity'])

    if _is_ajax(request):
        return JsonResponse({'ok': True, **_cart_payload(cart)})
    return redirect('cart')


# ── Cart remove ───────────────────────────────────────────────────────────────

def remove_from_cart(request, book_id):
    cart = get_cart(request)
    deleted, _ = CartItem.objects.filter(cart=cart, book_id=book_id).delete()
    if not deleted:
        CartItem.objects.filter(cart=cart, id=book_id).delete()
    if _is_ajax(request):
        return JsonResponse({'ok': True, **_cart_payload(cart)})
    messages.info(request, 'Item removed from your cart.')
    return redirect('cart')


# ── Checkout ──────────────────────────────────────────────────────────────────

def checkout(request):
    """Collects shipping details, reduces stock, creates an Order, clears cart."""
    cart = get_cart(request)
    items = list(cart.items.select_related('book'))
    if not items:
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Re-fetch with row lock to check stock at purchase time
                    locked = {
                        b.pk: b for b in
                        Book.objects.select_for_update().filter(
                            pk__in=[i.book_id for i in items]
                        )
                    }
                    for i in items:
                        b = locked[i.book_id]
                        if i.quantity > b.stock:
                            raise ValueError(
                                f'Only {b.stock} copies of "{b.title}" left.'
                            )
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    order.total = sum((i.subtotal for i in items), Decimal('0'))
                    order.order_number = f'HB-{timezone.now().strftime("%Y%m%d%H%M%S")}'
                    order.status = 'placed'
                    order.save()
                    for i in items:
                        OrderItem.objects.create(
                            order=order,
                            book=i.book,
                            title=i.book.title,
                            price=i.book.price,
                            quantity=i.quantity,
                        )
                        Book.objects.filter(pk=i.book_id).update(
                            stock=F('stock') - i.quantity
                        )
                    cart.items.all().delete()
            except ValueError as exc:
                messages.error(request, str(exc))
                return redirect('cart')

            request.session['last_order_number'] = order.order_number
            return redirect('success', order_number=order.order_number)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'full_name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial)

    return render(request, 'cart/checkout.html', {
        'form': form,
        'items': items,
        'total': cart.total,
    })


# ── Order success ─────────────────────────────────────────────────────────────

def success(request, order_number):
    # Only the session that placed the order can view it
    if request.session.get('last_order_number') != order_number:
        return redirect('home')
    order = get_object_or_404(
        Order.objects.prefetch_related('items'), order_number=order_number
    )
    return render(request, 'cart/success.html', {'order': order, 'items': order.items.all()})
