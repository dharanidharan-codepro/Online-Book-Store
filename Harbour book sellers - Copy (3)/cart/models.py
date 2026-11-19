
from decimal import Decimal

from django.conf import settings
from django.db import models

from catalog.models import Book


# ── DB-backed cart (one per browser session) ─────────────────────────────────

class Cart(models.Model):
    """One cart per browser session (no user login required)."""
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(
            (i.subtotal for i in self.items.select_related('book')),
            Decimal('0.00'),
        )

    @property
    def total_items(self):
        return sum(i.quantity for i in self.items.all())

    def __str__(self):
        return f'Cart {self.session_key[:8]}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'book')

    @property
    def subtotal(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.book.title}'


# ── Orders ────────────────────────────────────────────────────────────────────

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('placed', 'Placed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    full_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    order_number = models.CharField(max_length=30, unique=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='placed')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def customer_name(self):
        return self.full_name

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number or f'Order #{self.pk}'


class OrderItem(models.Model):
    """Snapshot of the purchase so history survives book edits/deletes."""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.title}'
