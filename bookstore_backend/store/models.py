from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def _unique_slug(instance, source):
    base = slugify(source) or 'item'
    slug, n = base, 2
    Model = instance.__class__
    while Model.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f'{base}-{n}'
        n += 1
    return slug


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    author = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.00'))])
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books')
    stock = models.PositiveIntegerField(default=10)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal('0.0'),
                                 validators=[MinValueValidator(0), MaxValueValidator(5)])

    # Featured sections managed from the admin panel
    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_audiobook = models.BooleanField(default=False, help_text='Show in the Audiobooks section')
    audio_url = models.URLField(blank=True, help_text='Optional link to audio sample')

    # AI summary cache (filled by store.services.ai)
    ai_summary = models.TextField(blank=True)
    ai_summary_updated = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:book_detail', args=[self.slug])

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def cover_url(self):
        if self.cover_image and hasattr(self.cover_image, 'url') and self.cover_image.name:
            return self.cover_image.url
        from pathlib import Path
        from django.conf import settings
        cover_file = Path(settings.BASE_DIR) / 'static' / 'img' / 'covers' / f'{self.slug}.svg'
        if cover_file.is_file():
            return f'/static/img/covers/{self.slug}.svg'
        return '/static/img/cover-placeholder.svg'

    def __str__(self):
        return f'{self.title} - {self.author}'


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class Cart(models.Model):
    """One cart per browser session (no user login required)."""
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum((i.subtotal for i in self.items.select_related('book')), Decimal('0.00'))

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


class Order(models.Model):
    STATUS_CHOICES = [('placed', 'Placed'), ('cancelled', 'Cancelled')]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='placed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} - {self.full_name}'


class OrderItem(models.Model):
    """Snapshot of the purchase so history survives book edits/deletes."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.title}'
