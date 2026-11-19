from decimal import Decimal
from django.core.management.base import BaseCommand
from catalog.models import Book, Category, Offer

DATA = {
    'Fiction': [
        ('The Alchemist', 'Paulo Coelho', '299', True, False, False,
         'A magical story about following your dreams and listening to your heart.',
         'An Andalusian shepherd boy named Santiago travels from his homeland in Spain to the Egyptian desert in search of treasure buried near the Pyramids.'),
        ('To Kill a Mockingbird', 'Harper Lee', '349', False, True, False,
         'A classic story of justice, racial injustice, and innocence.',
         'Set in the fictional town of Maycomb, Alabama, Atticus Finch defends an innocent Black man accused of a terrible crime.'),
        ('The Great Gatsby', 'F. Scott Fitzgerald', '279', True, False, False,
         'A tragic story of love, wealth, and the roaring twenties.',
         'Narrated by Nick Carraway, exploring the mysterious millionaire Jay Gatsby and his obsession with Daisy Buchanan.'),
    ],
    'Non-fiction': [
        ('Sapiens', 'Yuval Noah Harari', '499', True, False, True,
         'A brief history of humankind from the Stone Age to Silicon Valley.',
         'Explores how biology and history have defined us and enhanced our understanding of what it means to be human.'),
        ('Atomic Habits', 'James Clear', '399', True, True, True,
         'An easy and proven way to build good habits and break bad ones.',
         'Practical strategies to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results.'),
        ('Deep Work', 'Cal Newport', '420', False, True, False,
         'Rules for focused success in a distracted world.',
         'The ability to focus without distraction on a cognitively demanding task is a superpower in the modern economy.'),
    ],
    'Education': [
        ('Concepts of Physics', 'H.C. Verma', '450', False, False, False,
         'Foundational physics textbook for curious students and competitive exam aspirants.',
         'Comprehensive explanations of physics mechanics, optics, and electrodynamics.'),
    ],
    'Tech': [
        ('Clean Code', 'Robert C. Martin', '699', False, True, False,
         'A handbook of agile software craftsmanship.',
         'Even bad code can function. But if code isn’t clean, it can bring a development organization to its knees.'),
        ('Python Crash Course', 'Eric Matthes', '599', False, True, False,
         'A hands-on, project-based introduction to programming.',
         'A fast-paced, thorough introduction to Python that will have you writing programs, solving problems, and making things that work in no time.'),
        ('Designing Data-Intensive Applications', 'Martin Kleppmann', '899', True, True, False,
         'The big ideas behind reliable, scalable, and maintainable systems.',
         'A deep dive into distributed systems, storage engines, replication, partitioning, and stream processing.'),
    ],
}


class Command(BaseCommand):
    help = 'Load demo categories, books, and marketplace offers into Harbour Books.'

    def handle(self, *args, **opts):
        created_books = 0
        for cat_name, books in DATA.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            for title, author, price, best, new, audio, desc, syn in books:
                book, created = Book.objects.get_or_create(
                    title=title,
                    defaults=dict(
                        author=author,
                        price=Decimal(price),
                        category=cat,
                        description=desc,
                        synopsis=syn,
                        stock=25,
                        is_best_seller=best,
                        is_new_arrival=new,
                        is_audiobook=audio,
                    )
                )
                if created:
                    created_books += 1
                    Offer.objects.create(
                        book=book,
                        seller_name='Harbour Direct',
                        condition='new',
                        price=book.price,
                        shipping_cost=Decimal('0.00'),
                    )
                    Offer.objects.create(
                        book=book,
                        seller_name='Vintage Reads Co.',
                        condition='used_good',
                        price=Decimal(int(book.price * Decimal('0.85'))),
                        shipping_cost=Decimal('29.00'),
                    )

        self.stdout.write(self.style.SUCCESS(f'Demo data loaded: {created_books} books created.'))
