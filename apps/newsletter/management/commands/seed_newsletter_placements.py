from django.core.management.base import BaseCommand

from apps.newsletter.models import NewsletterPlacement

PLACEMENTS = [
    {
        "key": "hero_subscribe",
        "title": "Get Ayrshire's stories first.",
        "description": "",
        "cta_text": "Subscribe Free",
        "incentive_text": "",
        "style": "compact",
    },
    {
        "key": "rail_primary",
        "title": "Get the Newsletter",
        "description": "Local stories delivered every Friday. Free. No spam.",
        "cta_text": "Subscribe",
        "incentive_text": "",
        "style": "compact",
    },
    {
        "key": "footer_cta",
        "title": "Don't Miss a Thing",
        "description": "Your weekly dose of what's happening in Ayrshire, delivered every Friday. Takes 5 minutes to read.",
        "cta_text": "Subscribe Free",
        "incentive_text": "Free. No spam. Unsubscribe any time.",
        "style": "full",
    },
    {
        "key": "footer_global",
        "title": "Subscribe to Loudoun Proud",
        "description": "",
        "cta_text": "Subscribe",
        "incentive_text": "Free. Every Friday. No spam.",
        "style": "compact",
    },
    {
        "key": "article_footer",
        "title": "Enjoyed this story?",
        "description": "Get stories like this delivered to your inbox every Friday.",
        "cta_text": "Subscribe Free",
        "incentive_text": "No spam. Unsubscribe anytime.",
        "style": "full",
    },
]


class Command(BaseCommand):
    help = "Seed newsletter placements with initial data"

    def handle(self, *args, **options):
        created = 0
        for data in PLACEMENTS:
            _, was_created = NewsletterPlacement.objects.get_or_create(
                key=data["key"],
                defaults=data,
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {created} new placement(s) ({len(PLACEMENTS)} total defined).")
        )
