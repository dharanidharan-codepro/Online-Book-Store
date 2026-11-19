from django.test import TestCase
from django.urls import reverse

from .models import Book, Category


class BookSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category, _ = Category.objects.get_or_create(
            slug='fantasy',
            defaults={'name': 'Fantasy'},
        )
        mystery, _ = Category.objects.get_or_create(
            slug='mystery',
            defaults={'name': 'Mystery'},
        )
        cls.expensive = Book.objects.create(
            title='Zulu Tale',
            author='A. Reader',
            slug='zulu-tale',
            price='20.00',
            category=category,
            is_best_seller=True,
        )
        cls.cheapest = Book.objects.create(
            title='Alpha Tale',
            author='B. Reader',
            slug='alpha-tale',
            price='5.00',
            description='A secret dragon story',
        )
        cls.mystery_book = Book.objects.create(
            title='Midnight Case',
            author='C. Reader',
            slug='midnight-case',
            price='12.00',
            category=mystery,
        )

    def test_best_price_sort_orders_books_by_lowest_price(self):
        response = self.client.get(reverse('books'), {'sort': 'price_asc'})
        self.assertEqual(
            list(response.context['books']),
            [self.cheapest, self.mystery_book, self.expensive],
        )

    def test_featured_sort_prioritizes_best_sellers(self):
        response = self.client.get(reverse('books'), {'sort': 'featured'})
        self.assertEqual(
            list(response.context['books']),
            [self.expensive, self.mystery_book, self.cheapest],
        )

    def test_deep_search_includes_book_descriptions(self):
        response = self.client.get(
            reverse('books'),
            {'q': 'dragon', 'deep_search': '1'},
        )
        self.assertEqual(list(response.context['books']), [self.cheapest])

    def test_regular_search_does_not_match_book_descriptions(self):
        response = self.client.get(reverse('books'), {'q': 'dragon'})
        self.assertEqual(list(response.context['books']), [])

    def test_multiple_categories_filter_books_and_remain_checked(self):
        response = self.client.get(
            reverse('books'),
            {'category': ['fantasy', 'mystery']},
        )
        self.assertEqual(
            set(response.context['books']),
            {self.expensive, self.mystery_book},
        )
        self.assertEqual(
            response.context['selected_categories'],
            ['fantasy', 'mystery'],
        )
        self.assertContains(response, 'Find your story')
