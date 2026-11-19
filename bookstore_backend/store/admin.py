import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Book, Category, Order, OrderItem, Subscriber


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'stock', 'rating',
                    'is_best_seller', 'is_new_arrival', 'is_audiobook')
    list_editable = ('price', 'stock', 'is_best_seller', 'is_new_arrival', 'is_audiobook')
    list_filter = ('category', 'is_best_seller', 'is_new_arrival', 'is_audiobook')
    search_fields = ('title', 'author')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'ai_summary_updated')
    actions = ['clear_ai_summary']

    @admin.action(description='Clear cached AI summary (regenerates on next view)')
    def clear_ai_summary(self, request, queryset):
        queryset.update(ai_summary='', ai_summary_updated=None)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    actions = ['export_csv']

    @admin.action(description='Export selected emails as CSV')
    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
        w = csv.writer(resp)
        w.writerow(['email', 'subscribed_at', 'is_active'])
        for s in queryset:
            w.writerow([s.email, s.subscribed_at.isoformat(), s.is_active])
        return resp


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('book', 'title', 'price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'total', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'email')
    readonly_fields = ('total', 'created_at')
    inlines = [OrderItemInline]
