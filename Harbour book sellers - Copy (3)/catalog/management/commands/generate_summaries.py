from django.core.management.base import BaseCommand
from catalog.models import Book
from ai_summary.services import get_book_summary, AIServiceError
import time

class Command(BaseCommand):
    help = 'Generate and populate Gemini AI summaries for books in the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate summaries even if already present',
        )

    def handle(self, *args, **options):
        force = options['force']
        books = Book.objects.all().order_by('id')
        if not force:
            books = books.filter(ai_summary__isnull=True) | books.filter(ai_summary__exact='')

        count = books.count()
        self.stdout.write(self.style.NOTICE(f'Found {count} books needing summary.'))

        for book in books:
            self.stdout.write(f"Generating summary for '{book.title}' by {book.author}...")
            try:
                summary = get_book_summary(book.title, book.author)
                book.ai_summary = summary
                book.save(update_fields=['ai_summary'])
                self.stdout.write(self.style.SUCCESS(f"  ✓ Saved ({len(summary)} chars)"))
            except AIServiceError as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Failed: {e}"))
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Finished processing book summaries.'))

