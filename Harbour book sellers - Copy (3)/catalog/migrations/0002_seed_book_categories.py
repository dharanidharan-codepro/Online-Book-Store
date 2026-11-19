from django.db import migrations
from django.utils.text import slugify


CATEGORY_NAMES = [
    'Fiction',
    'Literary Fiction',
    'Adventure',
    'Mystery',
    'Personal Growth',
    'Romance',
    'Science',
    'Fantasy',
    'Children',
    'Lifestyle',
]


def add_default_categories(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    database = schema_editor.connection.alias
    for name in CATEGORY_NAMES:
        Category.objects.using(database).get_or_create(
            slug=slugify(name),
            defaults={'name': name},
        )


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, migrations.RunPython.noop),
    ]
