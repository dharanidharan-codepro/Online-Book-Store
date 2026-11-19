
from django.contrib import admin

from .models import Book, Category, Offer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'price', 'stock',
        'is_best_seller', 'is_new_arrival', 'is_audiobook', 'condition',
    )
    list_editable = ('price', 'stock', 'is_best_seller', 'is_new_arrival', 'is_audiobook')
    list_filter = ('category', 'is_best_seller', 'is_new_arrival', 'is_audiobook', 'condition')
    search_fields = ('title', 'author', 'isbn')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at',)
    actions = ['clear_ai_summary']

    @admin.action(description='Clear cached AI summary (regenerates on next view)')
    def clear_ai_summary(self, request, queryset):
        queryset.update(ai_summary='')


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1
    fields = ('seller_name', 'condition', 'price', 'shipping_cost', 'buy_url')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('seller_name', 'book', 'condition', 'price', 'shipping_cost', 'total_cost')
    list_filter = ('condition',)
    search_fields = ('seller_name', 'book__title')

    def total_cost(self, obj):
        return obj.total_cost
    total_cost.short_description = 'Total cost'
