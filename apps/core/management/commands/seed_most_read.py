from django.core.management.base import BaseCommand

from apps.articles.models import Article
from apps.core.most_read import seed_from_cards


class Command(BaseCommand):
    help = "Seed Most Read sorted sets with published articles"

    def handle(self, *args, **options):
        cards = list(
            Article.objects.filter(
                status="published",
                exclude_from_most_read=False,
            ).order_by("sort_order", "-created")
        )

        if not cards:
            self.stdout.write(self.style.WARNING("No published articles to seed."))
            return

        success = seed_from_cards(cards)
        if success:
            self.stdout.write(
                self.style.SUCCESS(f"Seeded Most Read with {len(cards)} articles.")
            )
        else:
            self.stdout.write(
                self.style.ERROR("Redis unavailable — start Redis and try again.")
            )
