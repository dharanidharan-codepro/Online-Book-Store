from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import Book, Cart, Category, Order, Subscriber
from .services.ai import AIServiceError


class StoreTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Tech')
        self.book = Book.objects.create(title='Clean Code', author='Martin', price=Decimal('100'),
                                        category=self.cat, stock=3, is_best_seller=True)

    def test_slug_auto_generated_and_unique(self):
        b2 = Book.objects.create(title='Clean Code', author='X', price=1, category=self.cat)
        self.assertNotEqual(self.book.slug, b2.slug)

    def test_pages_load(self):
        for url in [reverse('store:home'), reverse('store:book_list'),
                    reverse('store:category', args=['tech']), self.book.get_absolute_url(),
                    reverse('store:cart')]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_search_and_section_filter(self):
        r = self.client.get(reverse('store:book_list'), {'q': 'clean', 'section': 'best_sellers'})
        self.assertContains(r, 'Clean Code')
        r = self.client.get(reverse('store:book_list'), {'q': 'nothing'})
        self.assertNotContains(r, 'Clean Code')

    def test_subscribe(self):
        self.client.post(reverse('store:subscribe'), {'email': 'A@x.com'})
        self.client.post(reverse('store:subscribe'), {'email': 'a@x.com'})
        self.assertEqual(Subscriber.objects.count(), 1)
        r = self.client.post(reverse('store:subscribe'), {'email': 'bad'},
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 400)

    def test_cart_stock_cap_and_checkout(self):
        add = reverse('store:cart_add', args=[self.book.id])
        r = self.client.post(add, {'quantity': 10}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.json()['cart_count'], 3)  # capped at stock
        r = self.client.post(reverse('store:checkout'),
                             {'full_name': 'Ann', 'email': 'a@x.com', 'address': 'Chennai'})
        order = Order.objects.get()
        self.assertRedirects(r, reverse('store:order_success', args=[order.id]))
        self.assertEqual(order.total, Decimal('300'))
        self.book.refresh_from_db()
        self.assertEqual(self.book.stock, 0)
        self.assertEqual(Cart.objects.get().items.count(), 0)

    def test_empty_checkout_redirects(self):
        self.assertRedirects(self.client.get(reverse('store:checkout')), reverse('store:cart'))

    def test_summary_cached(self):
        url = reverse('store:book_summary', args=[self.book.slug])
        with patch('store.views.get_book_summary', return_value='Great book') as m:
            self.assertEqual(self.client.get(url).json()['cached'], False)
            self.assertEqual(self.client.get(url).json()['cached'], True)
            self.assertEqual(m.call_count, 1)

    def test_summary_error(self):
        with patch('store.views.get_book_summary', side_effect=AIServiceError('down')):
            r = self.client.get(reverse('store:book_summary', args=[self.book.slug]))
        self.assertEqual(r.status_code, 502)
