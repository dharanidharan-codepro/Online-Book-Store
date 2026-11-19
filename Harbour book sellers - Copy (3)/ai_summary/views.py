
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from catalog.models import Book
from .services import AIServiceError, get_book_summary


def summary_json(request, slug):
    """
    GET /summary/<slug>/          → return cached or freshly generated AI summary.
    GET /summary/<slug>/?refresh=1 → force-regenerate even if cached.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'GET only'}, status=405)

    book = get_object_or_404(Book, slug=slug)

    if book.ai_summary and request.GET.get('refresh') != '1':
        return JsonResponse({'summary': book.ai_summary, 'cached': True})

    try:
        summary = get_book_summary(book.title, book.author)
    except AIServiceError as exc:
        return JsonResponse({'error': str(exc)}, status=502)

    book.ai_summary = summary
    book.save(update_fields=['ai_summary'])
    return JsonResponse({'summary': summary, 'cached': False})
