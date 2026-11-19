from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .cart import get_cart
from .forms import CheckoutForm, SubscribeForm
from .models import Book, CartItem, Category, Order, OrderItem, Subscriber
from .services.ai import AIServiceError, get_book_summary

SECTION_SIZE = 8
PAGE_SIZE = 12
SORTS = {
    'new': '-created_at',
    'price_asc': 'price',
    'price_desc': '-price',
    'rating': '-rating',
    'title': 'title',
}


def _is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


def _cart_payload(cart):
    return {'cart_count': cart.total_items, 'cart_total': str(cart.total)}


# ---------------------------------------------------------------- home / books
@require_GET
def home(request):
    books = Book.objects.select_related('category')
    return render(request, 'store/home.html', {
        'best_sellers': books.filter(is_best_seller=True)[:SECTION_SIZE],
        'new_arrivals': books.filter(is_new_arrival=True)[:SECTION_SIZE],
        'audiobooks': books.filter(is_audiobook=True)[:SECTION_SIZE],
        'categories': Category.objects.all(),
        'subscribe_form': SubscribeForm(),
    })


@require_GET
def book_list(request, category_slug=None):
    books = Book.objects.select_related('category')
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)

    q = request.GET.get('q', '').strip()
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))

    section = request.GET.get('section')
    if section == 'best_sellers':
        books = books.filter(is_best_seller=True)
    elif section == 'new_arrivals':
        books = books.filter(is_new_arrival=True)
    elif section == 'audiobooks':
        books = books.filter(is_audiobook=True)

    sort = request.GET.get('sort', 'new')
    books = books.order_by(SORTS.get(sort, SORTS['new']))

    page = Paginator(books, PAGE_SIZE).get_page(request.GET.get('page'))
    return render(request, 'store/book_list.html', {
        'page_obj': page, 'books': page.object_list, 'category': category,
        'q': q, 'section': section, 'sort': sort,
    })


@require_GET
def book_detail(request, slug):
    book = get_object_or_404(Book.objects.select_related('category'), slug=slug)
    related = Book.objects.filter(category=book.category).exclude(pk=book.pk)[:4]
    return render(request, 'store/book_detail.html', {'book': book, 'related_books': related})


@require_GET
def book_summary(request, slug):
    """JSON endpoint: GET /books/<slug>/summary/[?refresh=1]. Cached in the DB."""
    book = get_object_or_404(Book, slug=slug)
    if book.ai_summary and request.GET.get('refresh') != '1':
        return JsonResponse({'summary': book.ai_summary, 'cached': True})
    try:
        summary = get_book_summary(book.title, book.author)
    except AIServiceError as exc:
        return JsonResponse({'error': str(exc)}, status=502)
    book.ai_summary = summary
    book.ai_summary_updated = timezone.now()
    book.save(update_fields=['ai_summary', 'ai_summary_updated'])
    return JsonResponse({'summary': summary, 'cached': False})


# ------------------------------------------------------------------ newsletter
@require_POST
def subscribe(request):
    form = SubscribeForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email'].lower()
        sub, created = Subscriber.objects.get_or_create(email=email)
        if not created and not sub.is_active:
            sub.is_active = True
            sub.save(update_fields=['is_active'])
        msg = 'Thanks for subscribing!' if created else 'You are already subscribed.'
        if _is_ajax(request):
            return JsonResponse({'ok': True, 'message': msg})
        messages.success(request, msg)
    else:
        err = 'Please enter a valid email address.'
        if _is_ajax(request):
            return JsonResponse({'ok': False, 'message': err}, status=400)
        messages.error(request, err)
    return redirect(request.META.get('HTTP_REFERER') or 'store:home')


# ------------------------------------------------------------------------ cart
@require_GET
def cart_detail(request):
    cart = get_cart(request)
    items = cart.items.select_related('book')
    return render(request, 'store/cart.html', {'cart': cart, 'items': items, 'total': cart.total})


def _parse_qty(request, default=1):
    try:
        return int(request.POST.get('quantity', default))
    except (TypeError, ValueError):
        return default


@require_POST
def cart_add(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    qty = max(_parse_qty(request), 1)
    cart = get_cart(request)
    item, _ = CartItem.objects.get_or_create(cart=cart, book=book, defaults={'quantity': 0})
    new_qty = min(item.quantity + qty, book.stock)
    if new_qty <= 0:
        item.delete()
        msg, ok = f'"{book.title}" is out of stock.', False
    else:
        item.quantity = new_qty
        item.save(update_fields=['quantity'])
        msg, ok = f'Added "{book.title}" to your cart.', True
    if _is_ajax(request):
        return JsonResponse({'ok': ok, 'message': msg, **_cart_payload(cart)}, status=200 if ok else 409)
    (messages.success if ok else messages.error)(request, msg)
    return redirect(request.META.get('HTTP_REFERER') or 'store:cart')


@require_POST
def cart_update(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    qty = _parse_qty(request)
    if qty <= 0:
        item.delete()
    else:
        item.quantity = min(qty, item.book.stock) or item.quantity
        item.save(update_fields=['quantity'])
    if _is_ajax(request):
        return JsonResponse({'ok': True, **_cart_payload(cart)})
    return redirect('store:cart')


@require_POST
def cart_remove(request, item_id):
    cart = get_cart(request)
    get_object_or_404(CartItem, pk=item_id, cart=cart).delete()
    if _is_ajax(request):
        return JsonResponse({'ok': True, **_cart_payload(cart)})
    messages.info(request, 'Item removed from your cart.')
    return redirect('store:cart')


# -------------------------------------------------------------------- checkout
def checkout(request):
    """Dummy checkout: creates an Order, reduces stock, empties the cart. No payment."""
    cart = get_cart(request)
    items = list(cart.items.select_related('book'))
    if not items:
        messages.info(request, 'Your cart is empty.')
        return redirect('store:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # re-fetch with a row lock, so stock is checked at purchase time
                    locked = {b.pk: b for b in
                              Book.objects.select_for_update().filter(pk__in=[i.book_id for i in items])}
                    for i in items:
                        b = locked[i.book_id]
                        if i.quantity > b.stock:
                            raise ValueError(f'Only {b.stock} copies of "{b.title}" left.')
                    order = form.save(commit=False)
                    order.total = sum((i.subtotal for i in items), 0)
                    order.save()
                    for i in items:
                        OrderItem.objects.create(order=order, book=i.book, title=i.book.title,
                                                 price=i.book.price, quantity=i.quantity)
                        Book.objects.filter(pk=i.book_id).update(stock=F('stock') - i.quantity)
                    cart.items.all().delete()
            except ValueError as exc:
                messages.error(request, str(exc))
                return redirect('store:cart')
            request.session['last_order_id'] = order.pk
            return redirect('store:order_success', order_id=order.pk)
    else:
        form = CheckoutForm()
    return render(request, 'store/checkout.html', {'form': form, 'items': items, 'total': cart.total})


@require_GET
def order_success(request, order_id):
    # only the browser session that placed the order can view it
    if request.session.get('last_order_id') != order_id:
        return redirect('store:home')
    order = get_object_or_404(Order.objects.prefetch_related('items'), pk=order_id)
    return render(request, 'store/order_success.html', {'order': order})
