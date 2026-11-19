
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Book(models.Model):
    CONDITION_CHOICES = [('new', 'New'), ('used_good', 'Used – Good'), ('used_fair', 'Used – Fair'), ('good', 'Good')]
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    title = models.CharField(max_length=220)
    author = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    isbn = models.CharField(max_length=30, blank=True, default='')
    description = models.TextField(blank=True)
    synopsis = models.TextField(blank=True)
    format = models.CharField(max_length=50, default='Paperback')
    pages = models.PositiveIntegerField(default=0)
    publisher = models.CharField(max_length=150, blank=True)
    publication_year = models.PositiveIntegerField(default=2024)
    language = models.CharField(max_length=50, default='English')
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    condition = models.CharField(max_length=30, choices=CONDITION_CHOICES, default='new')
    cover_image = models.ImageField(upload_to='books/', blank=True, null=True)
    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_audiobook = models.BooleanField(default=False)
    audio_url = models.URLField(blank=True, default='')
    ai_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def cover_url(self):
        if self.cover_image and hasattr(self.cover_image, 'url') and self.cover_image.name:
            return self.cover_image.url
        # Check for curated SVG cover in static/img/covers/<slug>.svg
        from pathlib import Path
        from django.conf import settings
        cover_file = Path(settings.BASE_DIR) / 'static' / 'img' / 'covers' / f'{self.slug}.svg'
        if cover_file.is_file():
            return f'/static/img/covers/{self.slug}.svg'
        return '/static/img/cover-placeholder.svg'

class Offer(models.Model):
    CONDITION_CHOICES = [('new', 'New'), ('used_good', 'Used – Good'), ('used_fair', 'Used – Fair'), ('good', 'Good')]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='offers')
    seller_name = models.CharField(max_length=120)
    condition = models.CharField(max_length=30, choices=CONDITION_CHOICES, default='used_good')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    buy_url = models.URLField(blank=True, default='')

    def __str__(self):
        return f'{self.seller_name} - {self.book.title}'

    @property
    def total_cost(self):
        return self.price + self.shipping_cost
