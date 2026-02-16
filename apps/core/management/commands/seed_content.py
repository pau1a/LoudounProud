from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.core.models import ContentCard, SiteSettings


class Command(BaseCommand):
    help = "Seed the database with placeholder content for Loudoun Proud"

    def handle(self, *args, **options):
        now = timezone.now()

        # Create or update SiteSettings
        settings = SiteSettings.load()
        settings.site_name = "Loudoun Proud"
        settings.tagline = "Your weekly dose of what's happening in Ayrshire"
        settings.hero_headline = "Ayrshire's stories, told by Ayrshire folk"
        settings.hero_subheadline = (
            "A free weekly newsletter covering Kilmarnock, Troon, Ayr, and everywhere "
            "in between. Local stories, events, and the people who make this place "
            "special — takes 5 minutes to read."
        )
        settings.newsletter_day = "Friday"
        settings.meta_description = (
            "Loudoun Proud — your free weekly Ayrshire community newsletter. "
            "Local stories, events, and community news from Kilmarnock, Troon, Ayr, and beyond."
        )
        settings.about_text = (
            "I'm Brian Kelly, and I've lived in Ayrshire my whole life. Born and raised "
            "in Kilmarnock, I've watched this community through its ups and downs — and "
            "I've always believed the best stories are the ones happening right on our "
            "doorstep.\n\n"
            "Loudoun Proud started with a simple idea: what if there was one place where "
            "you could find out what's actually going on around here? Not the national news "
            "with a Scottish angle, but the real local stuff — the new cafe opening on "
            "King Street, the school fundraiser in Galston, the planning application that "
            "might affect your street.\n\n"
            "Every week, I put together a newsletter that gives you the stories that matter "
            "to folk who live here. It takes about 5 minutes to read, and it's completely "
            "free. No clickbait, no doom-scrolling — just what's happening in your backyard, "
            "told by someone who genuinely cares about this place.\n\n"
            "Whether you're in Stewarton or Troon, Darvel or Irvine, Ayr or anywhere in "
            "between — this is your newsletter. Welcome to Loudoun Proud."
        )
        settings.hero_image = "heroimages/loudounhero.jpg"
        settings.save()
        self.stdout.write(self.style.SUCCESS("Created SiteSettings"))

        # Create sample content cards
        cards_data = [
            {
                "lead_style": "whats_happening",
                "headline": "Kilmarnock town centre gets £2.5m regeneration boost",
                "body_text": (
                    "East Ayrshire Council has confirmed a major investment in Kilmarnock's "
                    "town centre, with plans for new public spaces, improved pedestrian areas, "
                    "and support for local businesses. The work is expected to begin in spring "
                    "and will focus on the area around the Cross and King Street."
                ),
                "link_text": "Go deeper →",
                "sort_order": 0,
                "is_featured": True,
                "published_date": now - timedelta(hours=3),
            },
            {
                "lead_style": "why_it_matters",
                "headline": "New community hub planned for Galston",
                "body_text": (
                    "A disused building in the heart of Galston could be transformed into a "
                    "community hub with space for local groups, a cafe, and co-working area. "
                    "The project is being led by local residents and has already attracted "
                    "interest from the Scottish Government's Community Ownership Fund."
                ),
                "link_text": "Go deeper →",
                "sort_order": 1,
                "published_date": now - timedelta(hours=8),
            },
            {
                "lead_style": "one_fun_thing",
                "headline": "Troon beach named in Scotland's top 10 — again",
                "body_text": (
                    "Troon's South Beach has been named one of Scotland's best beaches for "
                    "the third year running. If you've ever spent a summer afternoon there "
                    "with an ice cream from the prom, you'll know exactly why. Perfect excuse "
                    "for a weekend trip when the weather plays ball."
                ),
                "link_text": "Go deeper →",
                "sort_order": 2,
                "published_date": now - timedelta(days=1),
            },
            {
                "lead_style": "icymi",
                "headline": "Darvel's wee independent bookshop celebrates first anniversary",
                "body_text": (
                    "The Irvine Valley Book Nook in Darvel marked one year of trading this "
                    "week, with owner Fiona MacLeod thanking the local community for keeping "
                    "independent retail alive. The shop has become a gathering spot for local "
                    "readers and hosts a monthly book club."
                ),
                "link_text": "Go deeper →",
                "sort_order": 3,
                "published_date": now - timedelta(days=2),
            },
        ]

        ContentCard.objects.all().delete()
        for card_data in cards_data:
            ContentCard.objects.create(**card_data)

        self.stdout.write(self.style.SUCCESS(f"Created {len(cards_data)} content cards"))
        self.stdout.write(self.style.SUCCESS("Seed complete!"))
