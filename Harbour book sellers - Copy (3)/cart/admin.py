
import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Cart, CartItem, Order, OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'total_items', 'created_at', 'updated_at')
    readonly_fields = ('session_key', 'created_at', 'updated_at')

    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = 'Items'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('book', 'title', 'price', 'quantity')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'total', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'email', 'order_number')
    readonly_fields = ('total', 'created_at', 'order_number')
    inlines = [OrderItemInline]
    actions = ['export_csv']

    @admin.action(description='Export selected orders as CSV')
    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="orders.csv"'
        w = csv.writer(resp)
        w.writerow(['order_number', 'full_name', 'email', 'total', 'status', 'created_at'])
        for o in queryset:
            w.writerow([o.order_number, o.full_name, o.email, o.total, o.status, o.created_at.isoformat()])
        return resp
