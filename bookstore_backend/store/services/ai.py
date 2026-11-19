"""
AI summary service  -- integration point for the AI teammate.

Contract used by the backend (do not change the signature):
    get_book_summary(title: str, author: str = '') -> str
    raises AIServiceError on any failure.

The default implementation below calls Google Gemini (AI Studio) over REST
using `requests`. The AI teammate can improve the prompt / model / parsing
freely as long as the contract above stays the same.
"""
import requests
from django.conf import settings


class AIServiceError(Exception):
    pass


def build_prompt(title, author=''):
    by = f' by {author}' if author else ''
    return (
        f'Write a concise, spoiler-free summary (about 100 words) of the book '
        f'"{title}"{by}. Mention the genre and who would enjoy it. '
        f'If you do not recognise this book, say so instead of inventing details.'
    )


def get_book_summary(title, author=''):
    if not settings.GEMINI_API_KEY:
        raise AIServiceError('GEMINI_API_KEY is not configured.')

    models_to_try = [settings.GEMINI_MODEL]
    if 'gemini-3.5-flash-lite' not in models_to_try:
        models_to_try.append('gemini-3.5-flash-lite')

    payload = {'contents': [{'parts': [{'text': build_prompt(title, author)}]}]}
    timeout = max(int(getattr(settings, 'GEMINI_TIMEOUT', 15)), 10)
    last_error = None

    for model in models_to_try:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
        try:
            resp = requests.post(
                url, json=payload, timeout=timeout,
                headers={'x-goog-api-key': settings.GEMINI_API_KEY},
            )
            if not resp.ok:
                last_error = f'HTTP {resp.status_code}: {resp.text[:120]}'
                continue
            data = resp.json()
            parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
            text = ''.join(p.get('text', '') for p in parts).strip()
            if text:
                return text
        except Exception as exc:
            last_error = str(exc)

    raise AIServiceError(f'Gemini request failed: {last_error or "Service unavailable"}')
