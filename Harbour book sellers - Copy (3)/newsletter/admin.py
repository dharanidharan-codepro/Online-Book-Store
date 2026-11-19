
import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    actions = ['export_csv', 'deactivate', 'reactivate']

    @admin.action(description='Export selected emails as CSV')
    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
        w = csv.writer(resp)
        w.writerow(['email', 'subscribed_at', 'is_active'])
        for s in queryset:
            w.writerow([s.email, s.subscribed_at.isoformat(), s.is_active])
        return resp

    @admin.action(description='Deactivate selected subscribers')
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='Reactivate selected subscribers')
    def reactivate(self, request, queryset):
        queryset.update(is_active=True)
