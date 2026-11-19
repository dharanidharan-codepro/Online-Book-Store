
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Subscriber


def subscribe(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        if email:
            sub, created = Subscriber.objects.get_or_create(email=email)
            if not created and not sub.is_active:
                sub.is_active = True
                sub.save(update_fields=['is_active'])
                msg = 'Welcome back! You have been re-subscribed.'
                messages.success(request, msg)
            elif created:
                msg = 'Thanks for subscribing!'
                messages.success(request, msg)
            else:
                msg = 'You are already subscribed.'
                messages.info(request, msg)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'ok': True, 'message': msg})
        else:
            msg = 'Please enter an email address.'
            messages.error(request, msg)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'ok': False, 'message': msg}, status=400)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)
