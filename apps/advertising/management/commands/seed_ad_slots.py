from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.advertising.models import AdCreative, AdSlot


class Command(BaseCommand):
    help = "Seed initial ad slots and house ads"

    def handle(self, *args, **options):
        now = timezone.now()
        one_year = now + timedelta(days=365)

        # --- Slots ---
        leaderboard, created = AdSlot.objects.get_or_create(
            name="leaderboard",
            defaults={
                "display_name": "Leaderboard (Below Lead Story)",
                "location": "Below lead story, above content rail",
                "width": 728,
                "height": 90,
                "is_responsive": True,
                "max_creatives": 3,
                "rotation_strategy": "sequential",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(f"  Created slot: {leaderboard.name}")

        rail_mpu, created = AdSlot.objects.get_or_create(
            name="rail-mpu",
            defaults={
                "display_name": "Rail MPU (Medium Rectangle)",
                "location": "Sidebar rail, below Most Read",
                "width": 300,
                "height": 250,
                "is_responsive": False,
                "max_creatives": 5,
                "rotation_strategy": "weighted",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(f"  Created slot: {rail_mpu.name}")

        section_break, created = AdSlot.objects.get_or_create(
            name="section-break",
            defaults={
                "display_name": "Section Break Leaderboard",
                "location": "Between main content and teaser sections",
                "width": 728,
                "height": 90,
                "is_responsive": True,
                "max_creatives": 2,
                "rotation_strategy": "random",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(f"  Created slot: {section_break.name}")

        # --- House ads ---
        AdCreative.objects.get_or_create(
            slot=leaderboard,
            name="Newsletter Signup — Leaderboard",
            defaults={
                "provider": "house",
                "creative_type": "html",
                "markup": (
                    '<div style="background:#1C1F24;color:#fff;padding:18px 24px;'
                    "text-align:center;border-radius:6px;font-family:inherit;"
                    'display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap">'
                    '<strong style="font-size:1rem">Get Ayrshire\u2019s weekly newsletter</strong>'
                    '<span style="font-size:0.875rem;opacity:0.8">'
                    "Local stories, zero spam. Every Friday.</span>"
                    '<a href="/subscribe/" style="background:#fff;color:#1C1F24;'
                    "padding:8px 20px;border-radius:4px;font-weight:600;"
                    'font-size:0.875rem;text-decoration:none">Subscribe Free</a>'
                    "</div>"
                ),
                "start_datetime": now,
                "end_datetime": one_year,
                "priority": 10,
                "weight": 1,
                "is_active": True,
            },
        )

        AdCreative.objects.get_or_create(
            slot=rail_mpu,
            name="Advertise With Us — Rail",
            defaults={
                "provider": "house",
                "creative_type": "html",
                "markup": (
                    '<div style="background:#F3F4F6;padding:32px 20px;text-align:center;'
                    'border:2px dashed #D1D5DB;border-radius:6px;font-family:inherit">'
                    '<strong style="font-size:1rem;color:#1C1F24;display:block;'
                    'margin-bottom:8px">Advertise Here</strong>'
                    '<span style="font-size:0.8125rem;color:#4B5563;display:block;'
                    'margin-bottom:12px">Reach Ayrshire\u2019s community</span>'
                    '<a href="/about/" style="color:#1C1F24;font-size:0.8125rem;'
                    'font-weight:600;text-decoration:underline">Learn More \u2192</a>'
                    "</div>"
                ),
                "target_url": "/about/",
                "start_datetime": now,
                "end_datetime": one_year,
                "priority": 5,
                "weight": 1,
                "is_active": True,
            },
        )

        AdCreative.objects.get_or_create(
            slot=section_break,
            name="Newsletter Signup — Section Break",
            defaults={
                "provider": "house",
                "creative_type": "html",
                "markup": (
                    '<div style="background:#1C1F24;color:#fff;padding:16px 24px;'
                    "text-align:center;border-radius:6px;font-family:inherit;"
                    'display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap">'
                    '<strong style="font-size:1rem">Don\u2019t miss a thing</strong>'
                    '<span style="font-size:0.875rem;opacity:0.8">'
                    "Ayrshire\u2019s stories, delivered free every Friday.</span>"
                    '<a href="/subscribe/" style="background:#fff;color:#1C1F24;'
                    "padding:8px 20px;border-radius:4px;font-weight:600;"
                    'font-size:0.875rem;text-decoration:none">Subscribe</a>'
                    "</div>"
                ),
                "start_datetime": now,
                "end_datetime": one_year,
                "priority": 10,
                "weight": 1,
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Ad slots and house ads seeded."))
