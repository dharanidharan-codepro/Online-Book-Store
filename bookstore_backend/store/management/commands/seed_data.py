from decimal import Decimal

from django.core.management.base import BaseCommand

from store.models import Book, Category

DATA = {
    'Fiction': [('The Alchemist', 'Paulo Coelho', '299', True, False, False),
                ('To Kill a Mockingbird', 'Harper Lee', '349', False, True, False)],
    'Non-fiction': [('Sapiens', 'Yuval Noah Harari', '499', True, False, True),
                    ('Atomic Habits', 'James Clear', '399', True, True, True)],
    'Education': [('Concepts of Physics', 'H.C. Verma', '450', False, False, False)],
    'Tech': [('Clean Code', 'Robert C. Martin', '699', False, True, False),
             ('Python Crash Course', 'Eric Matthes', '599', False, True, False)],
}


class Command(BaseCommand):
    help = 'Load demo categories and books.'

    def handle(self, *args, **opts):
        for cat_name, books in DATA.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            for title, author, price, best, new, audio in books:
                Book.objects.get_or_create(
                    title=title,
                    defaults=dict(author=author, price=Decimal(price), category=cat,
                                  description=f'{title} by {author}.', stock=25, rating=Decimal('4.5'),
                                  is_best_seller=best, is_new_arrival=new, is_audiobook=audio))
        self.stdout.write(self.style.SUCCESS('Demo data loaded.'))
