
import requests
from django.conf import settings


class AIServiceError(Exception):
    pass


# ── REST-based summary (compatible with bookstore_backend contract) ────────────

def _build_summary_prompt(title, author=''):
    by = f' by {author}' if author else ''
    return (
        f'Write a concise, spoiler-free summary (about 100 words) of the book '
        f'"{title}"{by}. Mention the genre and who would enjoy it. '
        f'If you do not recognise this book, say so instead of inventing details.'
    )


def get_book_summary(title, author=''):
    """
    REST-based Gemini summary. Raises AIServiceError on failure.
    This matches the contract from bookstore_backend/store/services/ai.py.
    """
    if not settings.GEMINI_API_KEY:
        raise AIServiceError('GEMINI_API_KEY is not configured.')

    candidate_models = [settings.GEMINI_MODEL, 'gemini-3.5-flash-lite', 'gemini-3-flash-preview', 'gemini-3.8-flash']
    models_to_try = []
    for m in candidate_models:
        if m and m not in models_to_try:
            models_to_try.append(m)

    payload = {'contents': [{'parts': [{'text': _build_summary_prompt(title, author)}]}]}
    timeout = max(int(getattr(settings, 'GEMINI_TIMEOUT', 25)), 15)
    last_error = None

    for model in models_to_try:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
        for attempt in range(2):
            try:
                resp = requests.post(
                    url, json=payload, timeout=timeout,
                    headers={'x-goog-api-key': settings.GEMINI_API_KEY, 'Content-Type': 'application/json'},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
                    text = ''.join(p.get('text', '') for p in parts).strip()
                    if text:
                        return text
                elif resp.status_code == 503:
                    last_error = f'HTTP 503 (model busy)'
                    continue
                else:
                    last_error = f'HTTP {resp.status_code}: {resp.text[:120]}'
                    break
            except Exception as exc:
                last_error = str(exc)

    raise AIServiceError(f'Gemini request failed: {last_error or "Service unavailable"}')


# ── SDK-based summary (used by the Readora AI assistant) ─────────────────────

def summarize_book(book, user_query=''):
    """
    Returns a cached or freshly generated AI summary for a Book instance.
    Tries the REST API first, falls back to a static description.
    """
    if book.ai_summary:
        return book.ai_summary

    try:
        summary = get_book_summary(book.title, book.author)
        # Cache the result on the book record
        book.ai_summary = summary
        book.save(update_fields=['ai_summary'])
        return summary
    except AIServiceError:
        pass

    # Final fallback: try the google-generativeai SDK if installed
    if settings.GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(settings.GEMINI_MODEL)
            category_name = book.category.name if book.category else 'general fiction'
            prompt = (
                f"Write a short, helpful summary for the book '{book.title}' "
                f"by {book.author}. Focus on readers who like {category_name}."
            )
            response = model.generate_content(prompt)
            return response.text.strip()[:700]
        except Exception:
            pass

    return (
        f"{book.title} by {book.author} offers a memorable reading experience, "
        f"with strong ideas, clear storytelling, and an engaging tone."
    )


# ── Readora AI assistant response ─────────────────────────────────────────────

def generate_book_response(books, message):
    """
    Generate an intelligent, friendly conversational reply from Readora AI
    using Google Gemini 3.5 Flash.
    """
    if not settings.GEMINI_API_KEY:
        if books:
            titles = ', '.join(f'"{b.title}" by {b.author}' for b in books[:3])
            return f'Here are matching books in our catalogue: {titles}.'
        return 'Readora AI is currently offline. Please configure GEMINI_API_KEY.'

    if books:
        books_context = '\n'.join([
            f'- "{b.title}" by {b.author} (Category: {b.category.name if b.category else "General"}, Price: ₹{b.price}): {b.description or b.synopsis or "Available in store"}'
            for b in books[:6]
        ])
    else:
        books_context = 'No direct keyword match, but you may recommend popular genres or ask clarifying questions.'

    prompt = (
        f"You are Readora AI, a delightful, knowledgeable, and helpful bookstore assistant for Harbour Books.\n"
        f"Books currently in our store catalogue:\n{books_context}\n\n"
        f"User message: \"{message}\"\n\n"
        f"Instructions:\n"
        f"1. Give a warm, friendly, conversational reply in under 120 words.\n"
        f"2. If recommending books, prioritize our store's books mentioned above with price and why they fit.\n"
        f"3. If the user greeting is casual (like 'hi', 'hello'), greet them warmly and suggest a couple of exciting reads from the list.\n"
        f"4. If asking for a budget (e.g. under ₹500), highlight our books that fit.\n"
        f"5. Maintain an enthusiastic, book-loving tone."
    )

    candidate_models = [settings.GEMINI_MODEL, 'gemini-3.5-flash-lite', 'gemini-3-flash-preview', 'gemini-3.8-flash']
    models_to_try = []
    for m in candidate_models:
        if m and m not in models_to_try:
            models_to_try.append(m)

    payload = {'contents': [{'parts': [{'text': prompt}]}]}
    timeout = max(int(getattr(settings, 'GEMINI_TIMEOUT', 25)), 15)

    # 1. REST call with candidate models
    for model in models_to_try:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
        try:
            resp = requests.post(
                url, json=payload, timeout=timeout,
                headers={'x-goog-api-key': settings.GEMINI_API_KEY, 'Content-Type': 'application/json'},
            )
            if resp.status_code == 200:
                data = resp.json()
                parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
                text = ''.join(p.get('text', '') for p in parts).strip()
                if text:
                    return text
        except Exception:
            pass

    # 2. SDK fallback
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
    except Exception:
        pass

    if books:
        titles = ', '.join(f'"{b.title}" by {b.author}' for b in books[:3])
        return f'Here are great titles available in our catalogue: {titles}. What kind of stories do you usually enjoy?'
    return "I'd love to help you find your next great read! Tell me your favorite genres, authors, or what mood you're in."
