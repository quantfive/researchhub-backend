from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from user.models import Author

class Command(BaseCommand):
    """
    Backfills user author score for each author
    """

    def handle(self, *args, **options):
        authorset = Author.objects.all()
        total_authors = authorset.count()
        for i, author in enumerate(authorset):
            if i < 370099:
                continue
            print('{} / {}'.format(i, total_authors))
            score = author.calculate_score()
            author.author_score = score
            author.save()