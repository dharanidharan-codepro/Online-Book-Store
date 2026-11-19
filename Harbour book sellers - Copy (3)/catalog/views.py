
import json
from decimal import Decimal

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from ai_summary.services import generate_book_response
from .models import Book, Category, Offer

def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)

def permission_denied(request, exception=None):
    return render(request, '403.html', status=403)

def server_error(request):
    return render(request, '500.html', status=500)

def home_page(request):
    books = Book.objects.order_by('-created_at')
    categories = Category.objects.order_by('name')
    best_sellers = books.filter(is_best_seller=True)[:4]
    new_arrivals = books.filter(is_new_arrival=True)[:4]
    audiobooks = books.filter(is_audiobook=True)[:4]
    seller_names = set(Offer.objects.values_list('seller_name', flat=True))
    context = {
        'featured_books': books[:2],
        'newest_books': books[:4],
        'books': books,
        'categories': categories,
        'best_sellers': best_sellers,
        'new_arrivals': new_arrivals,
        'audiobooks': audiobooks,
        'book_count': books.count(),
        'seller_count': len(seller_names) + 1,
    }
    return render(request, 'home.html', context)

def book_list(request):
    queryset = Book.objects.select_related('category').order_by('-created_at')
    q = request.GET.get('q', '').strip()
    deep_search = request.GET.get('deep_search') == '1'
    if q:
        search = Q(title__icontains=q) | Q(author__icontains=q) | Q(isbn__icontains=q)
        if deep_search:
            search |= (
                Q(description__icontains=q)
                | Q(synopsis__icontains=q)
                | Q(publisher__icontains=q)
                | Q(format__icontains=q)
                | Q(category__name__icontains=q)
            )
        queryset = queryset.filter(search)
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        queryset = queryset.filter(category__slug__in=selected_categories)
    featured = request.GET.get('featured')
    if featured == 'best_seller':
        queryset = queryset.filter(is_best_seller=True)
    elif featured == 'new_arrival':
        queryset = queryset.filter(is_new_arrival=True)
    elif featured == 'audiobook':
        queryset = queryset.filter(is_audiobook=True)
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort == 'title':
        queryset = queryset.order_by('title')
    elif sort == 'featured':
        queryset = queryset.order_by('-is_best_seller', '-is_new_arrival', '-created_at')
    min_price = request.GET.get('min_price')
    if min_price:
        queryset = queryset.filter(price__gte=Decimal(min_price))
    max_price = request.GET.get('max_price')
    if max_price:
        queryset = queryset.filter(price__lte=Decimal(max_price))
    conditions = request.GET.getlist('condition')
    if conditions:
        queryset = queryset.filter(condition__in=conditions)
    pagination_params = request.GET.copy()
    pagination_params.pop('page', None)
    paginator = Paginator(queryset, 12)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    return render(request, 'catalog/books.html', {'page_obj': page_obj, 'books': page_obj.object_list, 'q': q, 'categories': Category.objects.order_by('name'), 'selected_categories': selected_categories, 'sort': sort, 'featured': featured, 'deep_search': deep_search, 'count': queryset.count(), 'pagination_params': pagination_params.urlencode()})

def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category).order_by('-created_at')
    return render(request, 'catalog/category.html', {'category': category, 'books': books})

def book_detail(request, slug):
    book = get_object_or_404(Book.objects.prefetch_related('offers'), slug=slug)
    related_books = Book.objects.filter(category=book.category).exclude(pk=book.pk)[:4]
    if not related_books:
        related_books = Book.objects.exclude(pk=book.pk)[:4]
    return render(request, 'catalog/book_detail.html', {'book': book, 'related_books': related_books})

def assistant_page(request):
    return render(request, 'assistant.html', {'books': Book.objects.order_by('-created_at')[:8]})

@require_http_methods(['POST'])
def assistant_message(request):
    try:
        data = json.loads(request.body.decode('utf-8')) if request.body else {}
    except Exception:
        data = {}
    message = (data.get('message') or '').strip()
    if not message:
        return JsonResponse({'error': 'Please enter a message.'}, status=400)

    # 1. Search for matching books
    matches = list(Book.objects.filter(
        Q(title__icontains=message) |
        Q(author__icontains=message) |
        Q(isbn__icontains=message) |
        Q(category__name__icontains=message) |
        Q(description__icontains=message) |
        Q(synopsis__icontains=message)
    ).distinct()[:6])

    # If query mentions a budget like "under 500", find books within that budget
    import re
    price_match = re.search(r'under\s*₹?\s*(\d+)', message, re.IGNORECASE)
    if price_match:
        try:
            limit = Decimal(price_match.group(1))
            budget_matches = list(Book.objects.filter(price__lte=limit).order_by('price')[:6])
            if budget_matches:
                matches = budget_matches
        except Exception:
            pass

    # Supply relevant or featured catalogue books so Readora AI always has store context
    context_books = matches if matches else list(Book.objects.order_by('-is_best_seller', '-created_at')[:6])

    # Generate reply using Gemini 3.5 Flash
    reply_text = generate_book_response(context_books, message)

    return JsonResponse({
        'reply': reply_text,
        'books': [
            {
                'slug': b.slug,
                'title': b.title,
                'author': b.author,
                'price': str(b.price),
                'cover_url': b.cover_url
            }
            for b in (matches if matches else context_books[:3])
        ]
    })

@require_http_methods(['POST'])
def intro_seen(request):
    response = HttpResponseRedirect(request.POST.get('next') or request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('readora_intro', '1', max_age=31536000, samesite='Lax')
    return response

@require_http_methods(['POST'])
def cookie_consent(request):
    response = HttpResponseRedirect(request.POST.get('next') or request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('cookie_consent', '1', max_age=31536000, samesite='Lax')
    return response
